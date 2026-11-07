"""Integration test for the disposable GitHub Actions stack, never a live server."""
import base64
import os
from pathlib import Path
import subprocess
import urllib.request
import uuid

if os.environ.get('GITHUB_ACTIONS') != 'true' or os.environ.get('COMPOSE_PROJECT_NAME') != 'homeserver-ci':
    raise SystemExit('This test is restricted to the disposable homeserver-ci Actions project.')
root = Path(__file__).resolve().parents[1]
password = (root/'secrets/admin_password').read_text().strip()
authorization = 'Basic '+base64.b64encode(('ncadmin:'+password).encode()).decode()
filename = 'smoke-'+uuid.uuid4().hex+'.txt'
url = 'http://127.0.0.1:8080/remote.php/dav/files/ncadmin/'+filename
content = b'HomeServer disposable integration fixture\n'

def request(method, data=None):
    req = urllib.request.Request(url,data=data,method=method,headers={'Authorization':authorization})
    with urllib.request.urlopen(req,timeout=30) as response:
        return response.status,response.read()

assert request('PUT',content)[0] == 201
assert request('GET')[1] == content
subprocess.run(['docker','compose','restart','app'],cwd=root,check=True,timeout=150)
# Wait for app's real healthcheck instead of treating process startup as readiness.
import time
for _ in range(60):
    probe = subprocess.run(['python3',str(root/'tools/homeserver.py'),'check'],cwd=root,capture_output=True,timeout=60)
    if probe.returncode == 0:
        break
    time.sleep(3)
else:
    raise SystemExit('Application did not become ready after restart.')
assert request('GET')[1] == content
print('SMOKE_OK: authenticated WebDAV upload/download and app-restart persistence; fixture left in disposable volume.')
