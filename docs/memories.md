# Persistent Memories media tools

The optional [Dockerfile](../applications/media/Dockerfile) adds FFmpeg (including
ffprobe) and distribution ExifTool to the same pinned Nextcloud base. Both app and
cron must use this image. Installing packages interactively inside a running
container would be lost on recreation.

This uses software transcoding. GPU devices, face recognition, reverse-geocoding
downloads and bulk indexing are not automatically enabled. Review CPU, memory
and disk capacity before adding video workloads.

## Build and test without touching application data

Run from the repository root on Linux with Docker:

```sh
docker compose -f compose.yaml -f compose.memories.yaml build app
docker compose -f compose.yaml -f compose.memories.yaml config -q
docker run --rm --network none --read-only --user 33:33 \
  --memory 384m --cpus 1 --tmpfs /tmp:rw,nosuid,nodev,size=32m \
  --entrypoint sh homeserver-nextcloud-media:34.0.5 -ec '
    ffmpeg -hide_banner -loglevel error -threads 1 -f lavfi \
      -i testsrc=size=64x64:rate=2 -t 1 -an -c:v libx264 -threads 1 \
      -pix_fmt yuv420p /tmp/probe.mp4
    ffprobe -v error -show_entries stream=codec_name,width,height -of json /tmp/probe.mp4
    exiftool -ver
    exiftool -j -Duration /tmp/probe.mp4
  '
```

Expected: H.264, 64×64 pixels, ExifTool version and video metadata. This does not
test browser playback, every codec, hardware acceleration or large real files.
Apt repositories are not snapshot-pinned; record the built image ID and package
versions. The image is not guaranteed byte-for-byte reproducible.

## Activate after backup

After a verified coherent backup, schedule an interruption. For this repository's
stack (not an arbitrary existing deployment):

```sh
docker compose exec -T -u www-data app php occ maintenance:mode --on
docker compose stop cron
docker compose -f compose.yaml -f compose.memories.yaml up -d --no-deps app
# If the following fails, investigate; do not continue blindly.
docker compose -f compose.yaml -f compose.memories.yaml exec -T -u www-data app php occ maintenance:mode --off
docker compose -f compose.yaml -f compose.memories.yaml up -d --wait --wait-timeout 600
```

Do not use `--wait` while maintenance is enabled: the health check correctly
rejects maintenance mode. Check app and cron image IDs with `docker inspect`.
In **Administration settings → Memories**, configure:

| Setting | Value |
| --- | --- |
| ExifTool | `/usr/bin/exiftool` |
| FFmpeg | `/usr/bin/ffmpeg` |
| ffprobe | `/usr/bin/ffprobe` |

Use the admin interface for the other transcoding options. Verify a small photo
and video upload and playback using a daily account, then verify background jobs.
Memories handles subsequent indexing through upload hooks and Nextcloud cron;
do not add a second periodic indexing job. Keep Photos for album support.

Always include **both Compose files** for operations after activation, including
`up`, `exec` and updates. To upgrade Nextcloud, update the base image/digest in
both the main Compose file and this Dockerfile, update the overlay tag, rebuild
and retest before promotion. Changing only the main file leaves the overlay on
the old core. Keep a previous image/configuration for recovery; do not prune it
before validation. This image change does not replace a database backup strategy.

Sources: [Memories configuration](https://memories.gallery/config/),
[system options](https://memories.gallery/system-config/),
[hardware transcoding](https://memories.gallery/hw-transcoding/).
