FROM nextcloud:34.0.5-apache@sha256:515c072ea1cf82ece3503f301fdf75dd5a7148abcc8fa10aaefd5ec56643b703

# ffprobe is supplied by ffmpeg; use the distribution's ExifTool.
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg libimage-exiftool-perl \
 && rm -rf /var/lib/apt/lists/*
