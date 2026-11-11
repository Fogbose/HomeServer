import importlib.util
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

spec = importlib.util.spec_from_file_location('client_kit', Path(__file__).resolve().parents[1] / 'tools/build_client_kit.py')
kit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs)['href'])


class ClientKitTests(unittest.TestCase):
    def test_reject_invalid_origins_before_writing(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary) / 'kit'
            for value in ('http://cloud.example.org', 'https://user:pass@cloud.example.org',
                          'https://cloud.example.org/path', 'https://cloud.example.org?x=1',
                          'https://cloud.example.org#x', 'https://', 'https://cloud.example.org:0',
                          'https://cloud.example.org:65536', 'https://cloud.example.org:abc',
                          'https://cloud.example.org\\bad', 'https://cloud. example.org'):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    kit.build(value, out)
                self.assertFalse(out.exists())

    def test_portal_links_and_personalization(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = kit.build('https://cloud.example.org:8443/', Path(temporary) / 'kit')
            parser = Links()
            parser.feed((out / 'Start.html').read_text(encoding='utf-8'))
            apps = json.loads((out / 'catalogue.json').read_text(encoding='utf-8'))
            self.assertEqual(len(apps), 11)
            self.assertEqual(len({a['id'] for a in apps}), 11)
            for app in apps:
                self.assertIn(f'https://cloud.example.org:8443/index.php/apps/{app["id"]}/', parser.links)
            self.assertIn('Clients.md', parser.links)
            self.assertIn('https://cloud.example.org:8443/remote.php/dav',
                          (out / 'Clients.md').read_text(encoding='utf-8'))
            original = (out / 'Start.html').read_bytes()
            with self.assertRaises(FileExistsError):
                kit.build('https://other.example.org', out)
            self.assertEqual((out / 'Start.html').read_bytes(), original)
