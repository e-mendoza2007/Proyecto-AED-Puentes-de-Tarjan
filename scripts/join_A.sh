#!/bin/sh
# Video de la Parte A: Portada + Intro + Codigo + Demo.
# Uso (desde la raiz): sh scripts/run_all.sh
#                      manim -qh manim/credits.py Portada
#                      manim -qh manim/intro_A.py Intro
#                      manim -qh manim/codigo_A.py Codigo
#                      manim -qh manim/demo_A.py Demo
#                      sh scripts/join_A.sh
set -eu
V='media/videos'
LIST='lista_A.txt'
: > "$LIST"
for f in credits/1080p60/Portada intro_A/1080p60/Intro codigo_A/1080p60/Codigo demo_A/1080p60/Demo; do
  if [ ! -f "$V/$f.mp4" ]; then
    printf 'ERROR: falta %s/%s.mp4\n' "$V" "$f" >&2
    exit 1
  fi
  printf "file '%s/%s.mp4'\n" "$V" "$f" >> "$LIST"
done
ffmpeg -y -hide_banner -loglevel warning -f concat -safe 0 -i "$LIST" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart video_parteA.mp4
rm -f "$LIST"
if command -v ffprobe >/dev/null 2>&1; then
  printf 'Duracion: %s segundos\n' "$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 video_parteA.mp4)"
fi
printf '%s\n' 'Video generado: video_parteA.mp4'
