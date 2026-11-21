"""Utilidades comunes: carga de trazas JSON, dibujo del grafo y reproductores de eventos.
Las escenas NO calculan nada: solo reproducen los eventos emitidos por los programas C++."""
import json
from pathlib import Path

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent.parent
C_NODE, C_ACTIVE, C_DONE = BLUE_E, BLUE_C, GREEN_E
C_EDGE, C_TREE, C_BACK, C_BRIDGE, C_OK = GREY_B, BLUE_C, ORANGE, RED, GREEN_C


def load_trace(name):
    with open(ROOT / "traces" / f"{name}.json") as f:
        return json.load(f)


class GraphMob(VGroup):
    """Grafo no dirigido con soporte de aristas paralelas (arcos) y etiquetas de id opcionales."""

    def __init__(self, n, edges, pos, show_ids=False, radius=0.28):
        super().__init__()
        self.P = {v: np.array([pos[v][0], pos[v][1], 0.0]) for v in range(n)}
        self.E, self.EL, self.N = {}, {}, {}
        groups = {}
        for i, (u, v) in enumerate(edges):
            groups.setdefault((min(u, v), max(u, v)), []).append(i)
        for (a, b), ids in groups.items():
            k = len(ids)
            for j, i in enumerate(ids):
                if a == b:
                    continue  # autolazo: no se dibuja
                pa, pb = self.P[a], self.P[b]
                ang = (j - (k - 1) / 2) * 0.9
                mob = Line(pa, pb) if k == 1 else ArcBetweenPoints(pa, pb, angle=ang)
                mob.set_stroke(C_EDGE, width=5)
                self.E[i] = mob
                if show_ids:
                    d = pb - pa
                    right = np.array([d[1], -d[0], 0.0]) / (np.linalg.norm(d) + 1e-9)
                    sign = 1.0 if k == 1 else np.sign(ang)
                    lab = Text(f"e{i}", font_size=16, color=GREY_A)
                    lab.move_to(mob.point_from_proportion(0.5) + sign * right * 0.25)
                    self.EL[i] = lab
        for v in range(n):
            c = Circle(radius=radius).set_fill(C_NODE, 1).set_stroke(WHITE, 3)
            t = Text(str(v), font_size=26)
            node = VGroup(c, t).move_to(self.P[v])
            node.set_z_index(3)
            self.N[v] = node
        self.add(*self.E.values(), *self.EL.values(), *self.N.values())
        center = sum(self.P.values()) / max(n, 1)
        self.D = {}
        for v in range(n):
            d = self.P[v] - center
            nd = np.linalg.norm(d)
            d = d / nd if nd > 1e-6 else UP
            self.D[v] = UP if abs(d[1]) < 0.35 else d   # etiquetas hacia afuera (o arriba)

    def reset_nodes(self):
        for node in self.N.values():
            node[0].set_fill(C_NODE, 1)


class _Player:
    def __init__(self, scene, g, rt, counter=None):
        self.s, self.g, self.rt, self.counter, self.cap = scene, g, rt, counter, None

    def say(self, text, color=WHITE):
        new = Text(text, font_size=24, color=color).to_edge(DOWN, buff=0.4)
        if self.cap is not None:
            self.s.remove(self.cap)
        self.s.add(new)
        self.cap = new

    def bump(self, ev):
        if self.counter is not None and "ops" in ev:
            self.counter.become(Text(f"operaciones: {ev['ops']}", font_size=26, color=YELLOW).to_corner(UR))

    def run(self, events):
        for ev in events:
            getattr(self, "on_" + ev["t"])(ev)
            self.bump(ev)


class TarjanPlayer(_Player):
    """Reproduce la traza de Tarjan: muestra tin/low junto a cada nodo, back edges y puentes."""

    def __init__(self, scene, g, rt=0.45, counter=None):
        super().__init__(scene, g, rt, counter)
        self.tin, self.low, self.lab = {}, {}, {}

    def _mk(self, v):
        return Text(f"tin={self.tin[v]} low={self.low[v]}", font_size=20, color=YELLOW_B).move_to(
            self.g.P[v] + self.g.D[v] * 0.85)

    def _edge(self, e, color, width):
        return self.g.E[e].animate.set_stroke(color, width=width) if e in self.g.E else Wait(0.01)

    def on_new_root(self, ev):
        self.say(f"Nodo {ev['v']} sin visitar: lanzamos un nuevo DFS desde él")
        self.s.play(Indicate(self.g.N[ev["v"]], color=YELLOW), run_time=self.rt)

    def on_enter(self, ev):
        v = ev["v"]
        self.tin[v] = self.low[v] = ev["tin"]
        self.lab[v] = self._mk(v)
        self.say(f"Entramos a {v}: tin[{v}] = low[{v}] = {ev['tin']}")
        self.s.play(self.g.N[v][0].animate.set_fill(C_ACTIVE, 1), FadeIn(self.lab[v]), run_time=self.rt)

    def on_tree(self, ev):
        self.say(f"Arista de árbol {ev['u']} → {ev['v']}")
        self.s.play(self._edge(ev["e"], C_TREE, 8), run_time=self.rt)

    def on_back(self, ev):
        u, w = ev["u"], ev["v"]
        self.low[u] = ev["low"]
        self.lab[u].become(self._mk(u))
        self.say(f"Back edge {u} – {w}: low[{u}] = min(low[{u}], tin[{w}]) = {ev['low']}", C_BACK)
        self.s.play(self._edge(ev["e"], C_BACK, 8), Indicate(self.lab[u], color=C_BACK), run_time=self.rt)

    def on_low(self, ev):
        v = ev["v"]
        self.low[v] = ev["low"]
        self.lab[v].become(self._mk(v))
        self.say(f"Volvemos a {v}: low[{v}] = min(low[{v}], low[hijo]) = {ev['low']}")
        self.s.play(Indicate(self.lab[v]), run_time=self.rt)

    def on_check(self, ev):
        u, v, e = ev["u"], ev["v"], ev["e"]
        if ev["bridge"]:
            self.say(f"low[{v}] = {ev['lowv']} > tin[{u}] = {ev['tinu']}  →  ¡PUENTE!", C_BRIDGE)
            self.s.play(self._edge(e, C_BRIDGE, 12), run_time=self.rt * 1.5)
        else:
            self.say(f"low[{v}] = {ev['lowv']} ≤ tin[{u}] = {ev['tinu']}  →  no es puente", C_OK)
            self.s.play(self._edge(e, C_OK, 8), run_time=self.rt)

    def on_exit(self, ev):
        self.s.play(self.g.N[ev["v"]][0].animate.set_fill(C_DONE, 1), run_time=self.rt * 0.6)


class BrutePlayer(_Player):
    """Reproduce la traza de la fuerza bruta: quita una arista, corre BFS y restaura."""

    def __init__(self, scene, g, rt=0.12, counter=None):
        super().__init__(scene, g, rt, counter)
        self.bridge = {}

    def on_start(self, ev):
        self.say(f"Componentes conexas del grafo original: {ev['base']}")
        self.s.wait(self.rt * 4)

    def on_remove(self, ev):
        e = ev["e"]
        self.say(f"Quitamos la arista e{e} y corremos BFS desde cada nodo sin visitar")
        if e in self.g.E:
            self.s.play(self.g.E[e].animate.set_stroke(opacity=0.12), run_time=self.rt * 2)

    def on_visit(self, ev):
        self.s.play(self.g.N[ev["v"]][0].animate.set_fill(YELLOW_E, 1), run_time=self.rt)

    def on_check(self, ev):
        self.bridge[ev["e"]] = ev["bridge"]
        verdict, col = ("aumentan → PUENTE", C_BRIDGE) if ev["bridge"] else ("igual → no es puente", C_OK)
        self.say(f"Componentes sin e{ev['e']}: {ev['comps']} (original {ev['base']}) {verdict}", col)
        self.s.wait(self.rt * 3)

    def on_restore(self, ev):
        e = ev["e"]
        self.g.reset_nodes()
        if e in self.g.E:
            br = self.bridge.get(e, False)
            self.s.play(self.g.E[e].animate.set_stroke(C_BRIDGE if br else C_EDGE, width=10 if br else 5, opacity=1),
                        run_time=self.rt * 2)
