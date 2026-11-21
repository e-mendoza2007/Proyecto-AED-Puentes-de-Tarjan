#!/bin/sh
# Uso (desde la raiz):
#   sh scripts/run_all.sh           compila, genera trazas y prueba
#   sh scripts/run_all.sh render-b  renderiza solo las escenas de la Parte B
#   sh scripts/run_all.sh render    renderiza todas las escenas A+B (requiere A terminada)
set -eu
mkdir -p bin traces
TARJAN_SRC='src/tarjan_ref.cpp'
if [ -f src/tarjan.cpp ]; then
  TARJAN_SRC='src/tarjan.cpp'
else
  printf '%s\n' 'AVISO: falta src/tarjan.cpp; usando Tarjan de referencia SOLO para pruebas.'
fi
printf 'Compilando %s y src/brute.cpp\n' "$TARJAN_SRC"
g++ -O2 -std=c++17 -o bin/tarjan "$TARJAN_SRC"
g++ -O2 -std=c++17 -o bin/brute src/brute.cpp
for g in tree cycle parallel disconnected comparacion; do
  bin/tarjan < "graphs/$g.txt" > "traces/tarjan_$g.json"
  bin/brute  < "graphs/$g.txt" > "traces/brute_$g.json"
done
if [ -f graphs/demo.txt ]; then
  bin/tarjan < graphs/demo.txt > traces/tarjan_demo.json
fi
python3 scripts/cross_check.py
python3 scripts/make_scaling.py

if [ "${1:-}" = 'render' ]; then
  for p in src/tarjan.cpp manim/intro_A.py manim/demo_A.py graphs/demo.txt; do
    if [ ! -f "$p" ]; then
      printf 'ERROR: falta %s; para probar SOLO B usa render-b.\n' "$p" >&2
      exit 1
    fi
  done
fi
if [ "${1:-}" = 'render-b' ] || [ "${1:-}" = 'render' ]; then
  manim -qh manim/edge_cases.py CasoArbol CasoCiclo CasoParalelas CasoDesconectado
  manim -qh manim/complexity.py Complejidad
  if [ "${1:-}" = 'render' ]; then
    manim -qh manim/credits.py Portada Creditos
    manim -qh manim/intro_A.py Intro
    manim -qh manim/demo_A.py Demo
  fi
fi
