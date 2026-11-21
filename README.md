# Puentes (Tarjan) - Parte B: casos borde y comparacion con fuerza bruta
CS2023 - Algoritmos y Estructuras de Datos (UTEC, 2026-2)

## Software requerido
g++ (C++17), Python 3.9+, Manim Community (`pip install manim`), FFmpeg y Cairo/Pango (dependencias de Manim).
No se necesita LaTeX para las escenas (solo se usa `Text`).

## Contenido
- `src/brute.cpp`: fuerza bruta real, O(E(V+E)): quita cada arista y cuenta componentes con BFS.
- `src/tarjan_ref.cpp`: Tarjan de referencia para probar la Parte B (la Parte A lo reemplaza por el suyo).
- `graphs/`: tree, cycle, parallel, disconnected, comparacion.
- `scripts/`: `run_all.sh`, `cross_check.py`, `make_scaling.py`.
- `manim/`: `common.py`, `edge_cases.py`, `complexity.py`.

## Compilar y ejecutar
    sh scripts/run_all.sh            # compila, genera trazas, valida y genera scaling.json
    sh scripts/run_all.sh render     # ademas renderiza los videos (calidad alta, 1080p)

## Formato de entrada
`n m` y luego `m` lineas `u v` (0-indexado). El id de arista es el indice de la linea. Se permiten aristas paralelas, autolazos y nodos aislados.

## Contrato de traza (JSON por stdout; flag `--compact` = sin eventos)
`{"algo","n","edges":[[u,v]..],"bridges":[ids],"ops":N,"events":[..]}`
Eventos de Tarjan: `new_root{v}`, `enter{v,tin}`, `tree{u,v,e}`, `back{u,v,e,low}`, `low{v,low}`, `check{u,v,e,lowv,tinu,bridge}`, `exit{v}`.
Eventos de fuerza bruta: `start{base}`, `remove{e}`, `visit{v}`, `check{e,comps,base,bridge}`, `restore{e}`.
Todos llevan `ops`. Definicion de operacion: una entrada de adyacencia examinada + un nodo visitado/descubierto.

## Integración A+B (scripts ajustados)
El script detecta `src/tarjan.cpp` si existe; de lo contrario utiliza `src/tarjan_ref.cpp` solo para probar B.
- `sh scripts/run_all.sh`: compilar, regenerar trazas, contrastar 500 grafos y calcular operaciones.
- `sh scripts/run_all.sh render-b`: renderizar solo B, con la prueba anterior.
- `sh scripts/run_all.sh render`: renderizar A+B; requiere `src/tarjan.cpp`, `manim/intro_A.py`, `manim/demo_A.py`, `graphs/demo.txt`.
- `sh scripts/join.sh`: fusionar nueve videos y avisar si falta alguno o dura más de 5 minutos.
Consulta `GUIA_PARA_PARTE_B.md` para entender cada escena y preparar la entrega.
