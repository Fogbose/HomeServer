"""Generate an offline client portal. No credentials, downloads or installations."""
import argparse
import html
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def server_url(value):
    parts = urlsplit(value)
    if (parts.scheme != 'https' or not parts.hostname or parts.username is not None
            or parts.password is not None or parts.query or parts.fragment
            or parts.path not in ('', '/') or any(c.isspace() for c in value)
            or any(c in value for c in '\\<>"')):
        raise ValueError('Use an HTTPS origin, without credentials, path, query or fragment')
    if parts.port is not None and not 1 <= parts.port <= 65535:
        raise ValueError('Invalid port')
    return value.rstrip('/')


def build(server, output):
    server = server_url(server)
    apps = json.loads((ROOT / 'applications/catalogue.json').read_text(encoding='utf-8'))
    cards = ''.join(
        '<li><a href="{url}">{name}</a><p>{purpose}</p></li>'.format(
            url=html.escape(f'{server}/index.php/apps/{app["id"]}/', quote=True),
            name=html.escape(app['name']), purpose=html.escape(app['purpose']))
        for app in apps)
    page = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HomeServer applications</title><style>
body{font:1rem system-ui;margin:auto;padding:2rem;max-width:70rem;background:#f3f6fa;color:#17263b}
ul{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(14rem,1fr));gap:1rem}
li{padding:1.4rem;background:white;border-radius:1rem;border:1px solid #c6d1df}
a{color:#0757a6;font-weight:650}a:focus-visible{outline:3px solid #0757a6;outline-offset:4px}
</style><h1>HomeServer applications</h1><p>Connect to your private network first, then sign in to Nextcloud.</p>
<p>This portal stores no passwords and provides links, not offline application data.</p><ul>'''
    page += cards + '</ul><p>Client setup: <a href="Clients.md">Windows / Android / iOS guide</a></p></html>\n'
    # Refuse replacement of any existing output, including a partial earlier kit.
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output / 'Start.html').write_text(page, encoding='utf-8')
    guide = (ROOT / 'docs/clients.md').read_text(encoding='utf-8')
    guide = guide.replace('https://cloud.example.org', server)
    (output / 'Clients.md').write_text(guide, encoding='utf-8')
    (output / 'catalogue.json').write_text(json.dumps(apps, indent=2) + '\n', encoding='utf-8')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server', required=True, help='HTTPS origin, e.g. https://cloud.example.org')
    parser.add_argument('--output', required=True, help='New directory; keep personalized output private')
    args = parser.parse_args()
    try:
        build(args.server, args.output)
    except (ValueError, OSError) as error:
        parser.exit(1, f'Client kit not created: {error}\n')
    print('CLIENT_KIT_READY: open Start.html; no software installed or credentials configured.')


if __name__ == '__main__':
    main()
