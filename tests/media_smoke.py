"""Exercise the optional media image without network, ports or mounted data."""
import subprocess

probe = '''set -eu
ffmpeg -hide_banner -loglevel error -threads 1 -f lavfi \
  -i testsrc=size=64x64:rate=2 -t 1 -an -c:v libx264 -threads 1 \
  -pix_fmt yuv420p /tmp/probe.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height \
  -of csv=p=0 /tmp/probe.mp4 | grep -qx 'h264,64,64'
exiftool -ver
exiftool -j -Duration /tmp/probe.mp4
'''
subprocess.run([
    'docker', 'run', '--rm', '--network', 'none', '--read-only', '--user', '33:33',
    '--memory', '384m', '--cpus', '1', '--tmpfs', '/tmp:rw,nosuid,nodev,size=32m',
    '--entrypoint', 'sh', 'homeserver-nextcloud-media:34.0.5', '-ec', probe,
], check=True, timeout=120)
print('MEDIA_SMOKE_OK: H.264 encode/probe and ExifTool as www-data')
