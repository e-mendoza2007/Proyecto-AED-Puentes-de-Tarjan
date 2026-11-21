#!/bin/sh
# Fusiona A+B. Si falta algun clip, falla en vez de generar un video incompleto.
# Uso: sh scripts/join.sh (desde la raiz del repositorio; requiere ffmpeg y ffprobe)
set -eu
V='media/videos'
LIST='lista.txt'
: > "$LIST"
for f in \
  credits/1080p60/Portada \
  intro_A/1080p60/Intro \
  demo_A/1080p60/Demo \
  edge_cases/1080p60/CasoArbol \
  edge_cases/1080p60/CasoCiclo \
  edge_cases/1080p60/CasoParalelas \
  edge_cases/1080p60/CasoDesconectado \
  complexity/1080p60/Complejidad \
  credits/1080p60/Creditos; do
  if [ ! -f "$V/$f.mp4" ]; then
    printf 'ERROR: falta %s/%s.mp4\n' "$V" "$f" >&2
    printf '%s\n' 'Primero renderiza todas las escenas con: sh scripts/run_all.sh render' >&2
    exit 1
  fi
  printf "file '%s/%s.mp4'\n" "$V" "$f" >> "$LIST"
done
ffmpeg -y -hide_banner -loglevel warning -f concat -safe 0 -i "$LIST" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart video_final.mp4
if command -v ffprobe >/dev/null 2>&1; then
  D=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 video_final.mp4)
  printf 'Duracion final: %s segundos (limite: 300).\n' "$D"
  if ! awk -v x="$D" 'BEGIN {exit !(x <= 300)}'; then
    printf '%s\n' 'AVISO: el video supera los 5 minutos. Hay que acortar las escenas.' >&2
  fi
fi
printf '%s\n' 'Video generado: video_final.mp4'
