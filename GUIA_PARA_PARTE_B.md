# Guia de trabajo: Parte B — Puentes en grafos

## Qué pertenece a la Parte B
- `src/brute.cpp`: fuerza bruta real en C++.
- `manim/edge_cases.py`: los cuatro casos borde.
- `manim/complexity.py`: comparación animada Tarjan vs fuerza bruta; incluye ambas corridas.
- `manim/common.py`: reproductores de trazas compartidos con A; **coordinar antes de modificar**.
- `graphs/`, `traces/`, `scripts/`: entradas, eventos y verificación.
- `report/informe_B.tex`: aporte al informe; completar con datos y evidencias reales.

## Antes de instalar Manim: comprobar algoritmos
Desde la raíz de la carpeta `puentes`, en una terminal con g++, Python y `sh` (por ejemplo Git Bash/WSL en Windows):

```sh
sh scripts/run_all.sh
```

Salida esperada: `OK: 500 grafos aleatorios, Tarjan y fuerza bruta coinciden.`

**Aviso importante:** mientras no exista `src/tarjan.cpp`, el script usa `src/tarjan_ref.cpp` solo para pruebas. Al recibir A, colocar el programa real en `src/tarjan.cpp` y volver a ejecutar la validación.

## Instalar y probar Manim
Requisitos: Manim Community, FFmpeg y dependencias del entorno gráfico; ver documentación oficial: https://docs.manim.community/en/stable/installation/windows.html.

Desde la raíz del proyecto, probar una sola escena en baja resolución:

```sh
manim -pql manim/edge_cases.py CasoParalelas
```

El comando usa `-ql` (preview rápido) y `-p` para abrir el video. Se espera un `.mp4` en `media/videos/edge_cases/480p15/`.

Para generar los videos finales de B a 1080p60:

```sh
sh scripts/run_all.sh render-b
```

O escena por escena:

```sh
manim -qh manim/edge_cases.py CasoArbol CasoCiclo CasoParalelas CasoDesconectado
manim -qh manim/complexity.py Complejidad
```

## Qué muestra cada caso
- **Árbol (6 nodos, 5 aristas)**: todas son puentes; resultado `[0,1,2,3,4]`.
- **Ciclo (6 nodos, 6 aristas)**: ninguna es puente; resultado `[]`.
- **Paralelas**: `e1` y `e2` entre nodos 1 y 2 no son puentes; `e0` y `e3` sí, resultado `[0,3]`.
- **Desconectado**: tres componentes (incluido nodo aislado 6); puentes `[3,4]`. Tarjan debe comenzar un DFS por cada componente no visitada.

En `complexity.py`, para el mismo grafo de **V=8, E=9** se observaron **26 operaciones instrumentadas de Tarjan frente a 260 de fuerza bruta**, no segundos ni una medición de tiempo de pared.

## Qué narrar en cada animación de B
1. «En un árbol, al quitar cualquier arista, la red se parte. Por eso todas son puentes.»
2. «En un ciclo, siempre existe otro camino entre los extremos: no hay puentes.»
3. «Con dos aristas paralelas, quitar una todavía deja la otra conexión. Solo las aristas exteriores son puentes.»
4. «En un grafo desconectado lanzamos DFS desde cada nodo no visitado, no solo desde el primero.»
5. «Tarjan usa una sola exploración DFS, O(V+E). Fuerza bruta elimina cada arista y repite BFS: O(E(V+E)) para E>0.»

No es obligatorio narrar todas las escenas: la consigna permite texto en pantalla. Las escenas ya contienen subtítulos dinámicos; también puedes grabar una breve voz en off.

## Cómo integrar con A sin romper B
Solicitar al integrante A:
- `src/tarjan.cpp` con salida JSON igual a `src/tarjan_ref.cpp`.
- `manim/intro_A.py` con clase `Intro`.
- `manim/demo_A.py` con clase `Demo`.
- `graphs/demo.txt` para crear `traces/tarjan_demo.json`.
- Nombres de todos los integrantes en `manim/credits.py`.

Luego:

```sh
sh scripts/run_all.sh render
sh scripts/join.sh
```

`join.sh` exige los **nueve clips** en lugar de omitir silenciosamente los faltantes. Comprueba la duración final. **Máximo 5 minutos**.

## Antes de entregar
- Comprobar que las aristas paralelas se dibujan distintas y que los colores/etiquetas se leen en 1080p.
- Ver el `video_final.mp4` completo: orden, texto no cortado y máximo 300 segundos.
- Completar informe: carátula, descripción A, complejidad y casos B, nombres, 2 conclusiones, contribuciones, capturas reales, URL del repo y del video.
- Actualizar `README.md` para documentar el flujo real y usar los enlaces auténticos.
- Subir una sola entrega grupal a Gradescope **antes del 22 de noviembre de 2026, 20:00 (Lima)**.

## Límites de la revisión
La lógica C++ y la validación cruzada sí se ejecutaron. No se verificó el render de Manim porque Manim no está instalado en el entorno de revisión. Las escenas deben probarse en el equipo de uno de los integrantes antes de entregarse.
