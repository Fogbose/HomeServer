import importlib.util
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('homeserver',ROOT/'tools/homeserver.py')
hs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hs)


class InitializationTests(unittest.TestCase):
    def project(self,root):
        (root/'compose.yaml').write_text('services: {}',encoding='utf-8')
        (root/'.env.example').write_text('NC_TRUSTED_DOMAINS=localhost\n',encoding='utf-8')

    def test_creates_independent_credentials_without_printing_them(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.project(root)
            output = hs.initialize(root)
            db = (root/'secrets/db_password').read_text().strip()
            admin = (root/'secrets/admin_password').read_text().strip()
            self.assertGreaterEqual(len(db),48)
            self.assertNotEqual(db,admin)
            self.assertNotIn(db,output)
            self.assertNotIn(admin,output)
            self.assertEqual((root/'.env').read_text(),(root/'.env.example').read_text())
            if os.name == 'posix':
                self.assertEqual(stat.S_IMODE((root/'secrets').stat().st_mode),0o700)
                self.assertEqual(stat.S_IMODE((root/'.env').stat().st_mode),0o600)
            # Temporary fixture only: allow the OS cleanup to remove read-only files.
            for file in (root/'secrets').iterdir():
                file.chmod(0o600)

    def test_refuses_existing_environment_and_preserves_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.project(root)
            (root/'.env').write_text('KEEP_ME',encoding='utf-8')
            with self.assertRaises(ValueError):
                hs.initialize(root)
            self.assertEqual((root/'.env').read_text(),'KEEP_ME')
            self.assertFalse((root/'secrets').exists())

    def test_refuses_partial_initialization(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.project(root)
            (root/'secrets').mkdir()
            with self.assertRaises(ValueError):
                hs.initialize(root)
            self.assertFalse((root/'.env').exists())


class WakeTests(unittest.TestCase):
    def test_packet_has_correct_wire_format(self):
        packet = hs.magic_packet('02:11:22:33:44:55')
        self.assertEqual(len(packet),102)
        self.assertEqual(packet[:6],b'\xff'*6)
        self.assertEqual(packet[6:],bytes.fromhex('021122334455')*16)

    def test_invalid_or_multicast_mac_rejected(self):
        for mac in ('bad','00:00:00:00:00:00','01:11:22:33:44:55'):
            with self.assertRaises(ValueError):
                hs.magic_packet(mac)

    def test_preview_never_opens_socket(self):
        with patch.object(hs.socket,'socket',side_effect=AssertionError('network accessed')):
            self.assertIn('no packet sent',hs.wake('02:11:22:33:44:55','192.168.10.0/24','192.168.10.2'))

    def test_wrong_network_or_broadcast_source_rejected(self):
        for source in ('192.168.20.2','192.168.10.255'):
            with self.assertRaises(ValueError):
                hs.wake('02:11:22:33:44:55','192.168.10.0/24',source)


class DiagnosticsTests(unittest.TestCase):
    def rows(self):
        return [{'Service':name,'State':'running','Health':('' if name == 'cron' else 'healthy')}
                for name in ('app','db','redis','cron')]

    def test_accepts_array_and_newline_json(self):
        rows = self.rows()
        self.assertEqual(hs.service_state(json.dumps(rows)),hs.service_state('\n'.join(json.dumps(r) for r in rows)))

    def test_missing_stopped_unhealthy_and_duplicate_services_fail(self):
        scenarios = [self.rows()[:-1], self.rows()+[self.rows()[0]]]
        for key,value in [('State','exited'),('Health','unhealthy')]:
            rows = self.rows()
            rows[0][key] = value
            scenarios.append(rows)
        for rows in scenarios:
            with self.assertRaises(RuntimeError):
                hs.service_state(json.dumps(rows))

    def test_maintenance_fails_even_when_processes_healthy(self):
        with patch.object(hs,'compose',side_effect=[json.dumps(self.rows()),json.dumps({'installed':True,'maintenance':True,'needsDbUpgrade':False})]):
            with self.assertRaises(RuntimeError):
                hs.check(ROOT)

    def test_diagnostic_reports_limited_scope(self):
        with patch.object(hs,'compose',side_effect=[json.dumps(self.rows()),json.dumps({'installed':True,'maintenance':False,'needsDbUpgrade':False,'versionstring':'test'}),'PONG\n']):
            result = json.loads(hs.check(ROOT))
            self.assertIn('restore not verified',result['scope'])


if __name__ == '__main__':
    unittest.main()
