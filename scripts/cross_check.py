"""Validacion cruzada: compara los puentes de Tarjan contra la fuerza bruta en grafos aleatorios
(incluye aristas paralelas, autolazos y grafos desconectados)."""
import json, random, subprocess, sys
TARJAN = sys.argv[1] if len(sys.argv) > 1 else "bin/tarjan"
BRUTE = sys.argv[2] if len(sys.argv) > 2 else "bin/brute"

def run(exe, text):
    out = subprocess.run([exe, "--compact"], input=text, capture_output=True, text=True, check=True).stdout
    return json.loads(out)["bridges"]

random.seed(2026)
for t in range(500):
    n = random.randint(1, 9); m = random.randint(0, 14)
    edges = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
    text = f"{n} {m}\n" + "".join(f"{u} {v}\n" for u, v in edges)
    a, b = run(TARJAN, text), run(BRUTE, text)
    if a != b:
        print("DIFERENCIA en el grafo:\n" + text, "tarjan:", a, "brute:", b); sys.exit(1)
print("OK: 500 grafos aleatorios, Tarjan y fuerza bruta coinciden.")
