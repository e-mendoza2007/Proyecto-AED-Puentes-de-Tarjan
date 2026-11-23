# Detección de puentes en grafos — Algoritmo de Tarjan

**Proyecto Final 2 — CS2023: Algoritmos y Estructuras de Datos**  
**Universidad de Ingeniería y Tecnología (UTEC) · Ciclo 2026-II**

## Integrantes

- Mahir Gianpier Gutierrez Rodriguez
- Ernesto Yen Mendoza Aguilar

## Descripción

Este proyecto implementa en **C++17** el algoritmo de **Tarjan para detectar puentes en grafos no dirigidos**. Una arista es un puente si, al eliminarla, aumenta el número de componentes conexas del grafo.

Tarjan encuentra todos los puentes mediante DFS, los tiempos de descubrimiento `tin` y los valores `low`, con complejidad **O(V + E)**. Para verificar los resultados se implementó además un método de fuerza bruta que retira cada arista temporalmente y comprueba la conectividad mediante BFS, con complejidad **O(E · (V + E))**.

Los programas C++ exportan **trazas JSON de ejecuciones reales** que se utilizan para producir animaciones con **Manim Community**. El video ilustra la detección de puentes, casos especiales (árboles, ciclos, aristas paralelas y grafos desconectados) y la comparación entre los dos métodos.

**Repositorio:** https://github.com/e-mendoza2007/Proyecto-AED-Puentes-de-Tarjan.git

## Herramientas y requisitos

- Compilador **g++** con soporte para C++17.
- **Python 3**.
- **Manim Community** y sus dependencias (incluidas las necesarias para renderizar textos y gráficos).
- **FFmpeg** y, para comprobar la duración final, **ffprobe**.
- **Git Bash** o un shell compatible para ejecutar los scripts `.sh` (en Windows).

Instalación y verificación básica de Manim:

```bash
python -m pip install manim
manim --version
```

La guía oficial de instalación es https://docs.manim.community/en/stable/installation.html.

## Organización del código

```text
.
├── src/
│   ├── tarjan.cpp              # Detección de puentes por Tarjan
│   └── brute.cpp               # Validación por fuerza bruta
├── graphs/                     # Grafos de entrada, demostración y casos borde
├── manim/
│   ├── common.py               # Componentes visuales y lector de trazas
│   ├── intro_A.py              # Introducción
│   ├── codigo_A.py             # Explicación adicional del código
│   ├── demo_A.py               # Recorrido de Tarjan
│   ├── fuerza_bruta.py         # Demostración de fuerza bruta
│   ├── edge_cases.py           # Árbol, ciclo, paralelas y desconectado
│   ├── complexity.py           # Comparación de complejidad
│   └── credits.py              # Portada y créditos
├── scripts/
│   ├── run_all.sh              # Compilación, trazas y comprobación
│   ├── cross_check.py          # Validación cruzada
│   ├── make_scaling.py         # Datos de crecimiento
│   └── join.sh                 # Unión de 10 clips
└── README.md
```

Las carpetas `bin/`, `traces/` y `media/` se crean o actualizan durante la ejecución; sus archivos generados no son necesarios en el repositorio.

## Compilación y generación de trazas

1. Clonar el proyecto y entrar en su carpeta raíz:

   ```bash
   git clone https://github.com/e-mendoza2007/Proyecto-AED-Puentes-de-Tarjan.git
   cd Proyecto-AED-Puentes-de-Tarjan
   ```

2. Desde **Git Bash** (o un shell compatible), compilar, generar las trazas y ejecutar la validación:

   ```bash
   sh scripts/run_all.sh
   ```

   El script compila `src/tarjan.cpp` y `src/brute.cpp`, produce trazas JSON en `traces/`, ejecuta una comparación sobre **500 grafos aleatorios** y genera las mediciones de crecimiento.

   Si se ejecuta manualmente en Windows, asegúrese de tener disponibles `g++`, `python3` y `manim` en el entorno correspondiente.

**Formato de los grafos:** primera línea `n m` (número de vértices y aristas), seguida de `m` líneas `u v` con los extremos de cada arista, numerados desde cero. Se admiten aristas paralelas, lazos y vértices aislados.

## Renderizado de animaciones

Después de generar las trazas, ejecutar estos comandos **desde la raíz del repositorio**. La opción `-pqh` produce MP4 en alta calidad (1080p a 60 FPS) y abre el archivo al terminar.

```bash
manim -pqh manim/credits.py Portada
manim -pqh manim/intro_A.py Intro
manim -pqh manim/demo_A.py Demo
manim -pqh manim/fuerza_bruta.py FuerzaBruta
manim -pqh manim/edge_cases.py CasoArbol
manim -pqh manim/edge_cases.py CasoCiclo
manim -pqh manim/edge_cases.py CasoParalelas
manim -pqh manim/edge_cases.py CasoDesconectado
manim -pqh manim/complexity.py Complejidad
manim -pqh manim/credits.py Creditos
```

La escena adicional de explicación del código se puede generar con:

```bash
manim -pqh manim/codigo_A.py Codigo
```

El video de la **Parte A** (Portada + Intro + Codigo + Demo) se une con:

```bash
sh scripts/join_A.sh      # genera video_parteA.mp4
```

Los MP4 se guardan normalmente en `media/videos/<nombre_del_archivo>/1080p60/`.

## Unión del video

Una vez generados los 10 clips requeridos, ejecutar desde **Git Bash**:

```bash
sh scripts/join.sh
```

El script comprueba que existan todas las escenas y genera `video_final.mp4` mediante FFmpeg. Si `ffprobe` está disponible, muestra la duración total y avisa cuando supera el máximo de **5 minutos**. La narración y la edición de audio pueden incorporarse al video resultante.

## Validación y complejidad

| Método | Complejidad temporal | Función en el proyecto |
|---|---|---|
| Tarjan con DFS, `tin` y `low` | `O(V + E)` | Detección principal de puentes |
| Fuerza bruta con BFS | `O(E · (V + E))` | Comparación y verificación |

El script `scripts/cross_check.py` contrasta ambas implementaciones con 500 grafos aleatorios. La visualización también presenta los casos de árbol, ciclo, aristas paralelas y grafo desconectado.

## Video educativo

El MP4 final se obtiene ejecutando los comandos anteriores. **Agregar aquí el enlace público o de acceso compartido al video final antes de la entrega.**

## Referencias

- [Manim Community — documentación](https://docs.manim.community/en/stable/)
- [Manim Community — galería de ejemplos](https://docs.manim.community/en/stable/examples.html)
- [CP-Algorithms — Finding Bridges](https://cp-algorithms.com/graph/bridge-searching.html)
