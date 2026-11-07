#!/usr/bin/env python3
"""Small dependency-free helpers. No installers, destructive cleanup, or shutdown."""
import argparse
import ipaddress
import json
import os
from pathlib import Path
import re
import secrets
import socket
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def initialize(root):
    root = Path(root).resolve(strict=True)
    template = root / '.env.example'
    if not template.is_file() or not (root/'compose.yaml').is_file():
        raise ValueError('Not a HomeServer project directory.')
    destination = root/'secrets'
    if (root/'.env').exists() or (root/'.env').is_symlink() or destination.exists() or destination.is_symlink():
        raise ValueError('Existing .env or secrets directory: refusing to overwrite. Review it manually.')
    # The parent is private. Files are readable by container users through their
    # individual read-only Compose bind mounts, not by other host users through it.
    destination.mkdir(mode=0o700)
    values = {'db_name':'nextcloud','db_user':'nextcloud',
              'db_password':secrets.token_urlsafe(36),'admin_password':secrets.token_urlsafe(36)}
    for name,value in values.items():
        with (destination/name).open('x',encoding='ascii',newline='\n') as stream:
            stream.write(value+'\n')
        (destination/name).chmod(0o444)
    with (root/'.env').open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(template.read_text(encoding='utf-8'))
    (root/'.env').chmod(0o600)
    return 'INITIALIZED: review .env; credentials are in secrets/, never printed. No container started.'


def magic_packet(mac):
    if not re.fullmatch(r'(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}',mac):
        raise ValueError('MAC must contain six hexadecimal pairs separated by colons.')
    octets = bytes.fromhex(mac.replace(':',''))
    if octets == bytes(6) or octets[0] & 1:
        raise ValueError('A unicast, nonzero target MAC is required.')
    return b'\xff'*6 + octets*16


def wake(mac, network, source, send=False):
    packet = magic_packet(mac)
    subnet = ipaddress.IPv4Network(network,strict=True)
    address = ipaddress.IPv4Address(source)
    if subnet.prefixlen > 30 or address not in subnet or address in (subnet.network_address,subnet.broadcast_address):
        raise ValueError('Source must be a usable address in the specified broadcast LAN.')
    if not send:
        return f'PREVIEW: 102 bytes to {subnet.broadcast_address}:9 from {address}; no packet sent.'
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as client:
        # Binding fails when the explicitly selected address is not local.
        client.bind((str(address),0))
        client.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        if client.sendto(packet,(str(subnet.broadcast_address),9)) != 102:
            raise RuntimeError('Incomplete UDP send.')
    return 'PACKET_SENT: server wake-up and service availability still need verification.'


def compose(root, *arguments):
    result = subprocess.run(['docker','compose','--project-directory',str(root),*arguments],
                            capture_output=True,text=True,timeout=45,check=False)
    if result.returncode:
        # Do not echo arbitrary Docker output that could contain configuration.
        raise RuntimeError('Docker Compose command failed; check access and service state locally.')
    return result.stdout


def service_state(output):
    try:
        rows = json.loads(output)
        if isinstance(rows,dict):
            rows = [rows]
    except json.JSONDecodeError:
        rows = [json.loads(line) for line in output.splitlines() if line.strip()]
    if not isinstance(rows,list):
        raise ValueError('Unexpected Docker Compose process format.')
    result = {}
    for service in ('app','db','redis','cron'):
        matching = [row for row in rows if row.get('Service') == service]
        if len(matching) != 1 or matching[0].get('State') != 'running':
            raise RuntimeError(f'Service is missing, duplicated or not running: {service}')
        if service != 'cron' and matching[0].get('Health') != 'healthy':
            raise RuntimeError(f'Service is not healthy: {service}')
        result[service] = 'running' if service == 'cron' else 'healthy'
    return result


def check(root):
    result = service_state(compose(root,'ps','--all','--format','json'))
    status = json.loads(compose(root,'exec','-T','-u','www-data','app','php','occ','status','--output=json'))
    if status.get('installed') is not True or status.get('maintenance') is not False or status.get('needsDbUpgrade') is not False:
        raise RuntimeError('Nextcloud is not installed, in maintenance or requires a database upgrade.')
    if compose(root,'exec','-T','redis','redis-cli','ping').strip() != 'PONG':
        raise RuntimeError('Redis did not answer PONG.')
    return json.dumps({'services':result,'nextcloud':status.get('versionstring'),
                       'scope':'local app/db/cache/process state only; backup, HTTPS, cron execution and restore not verified'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    for command in ('init','check'):
        child = sub.add_parser(command)
        child.add_argument('--path',type=Path,default=ROOT)
    child = sub.add_parser('wake')
    child.add_argument('--mac',required=True)
    child.add_argument('--network',required=True,help='Explicit local IPv4 subnet, e.g. 192.168.10.0/24')
    child.add_argument('--source',required=True,help='IPv4 address on this sender')
    child.add_argument('--send',action='store_true',help='Actually transmit; omitted means preview only')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            print(initialize(args.path))
        elif args.command == 'check':
            print(check(args.path.resolve(strict=True)))
        else:
            print(wake(args.mac,args.network,args.source,args.send))
    except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as error:
        print(f'FAILED: {error}',file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
