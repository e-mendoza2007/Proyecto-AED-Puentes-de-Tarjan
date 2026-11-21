"""Genera traces/scaling.json: operaciones de Tarjan y fuerza bruta segun el tamano del grafo."""
import json, random, subprocess, sys
TARJAN = sys.argv[1] if len(sys.argv) > 1 else "bin/tarjan"
BRUTE = sys.argv[2] if len(sys.argv) > 2 else "bin/brute"
random.seed(7)
rows = []
for n in [8, 16, 32, 64, 128, 256, 512]:
    edges = [(random.randrange(i), i) for i in range(1, n)]            # arbol aleatorio (conexo)
    edges += [(random.randrange(n), random.randrange(n)) for _ in range(n // 2)]  # aristas extra
    text = f"{n} {len(edges)}\n" + "".join(f"{u} {v}\n" for u, v in edges)
    r = {"n": n, "m": len(edges)}
    for name, exe in (("tarjan", TARJAN), ("brute", BRUTE)):
        out = subprocess.run([exe, "--compact"], input=text, capture_output=True, text=True, check=True).stdout
        r[name + "_ops"] = json.loads(out)["ops"]
    rows.append(r); print(r)
json.dump(rows, open("traces/scaling.json", "w"), indent=1)
