"""Parte A - Demo paso a paso de Tarjan sobre graphs/demo.txt (8 nodos, 9 aristas).
Uso: manim -qh manim/demo_A.py Demo
Reproduce traces/tarjan_demo.json, generado por bin/tarjan (sh scripts/run_all.sh)."""
from common import *

DEMO_POS = {0: (-5.6, 1.0), 1: (-3.6, 1.0), 2: (-3.6, -1.0), 3: (-5.6, -1.0),
            4: (-1.4, -1.0), 5: (-0.3, 1.0), 6: (0.8, -1.0), 7: (3.0, -1.0)}
PILA_X, PILA_Y0 = 5.3, -2.3


class TarjanConPila(TarjanPlayer):
    """Igual que TarjanPlayer, pero ademas dibuja la pila de recursion del DFS."""

    def __init__(self, scene, g, rt=0.45, counter=None):
        super().__init__(scene, g, rt, counter)
        self.pila = []

    def on_enter(self, ev):
        v = ev["v"]
        self.tin[v] = self.low[v] = ev["tin"]
        self.lab[v] = self._mk(v)
        caja = VGroup(Rectangle(width=1.8, height=0.38).set_fill(BLUE_E, 0.6).set_stroke(WHITE, 2),
                      Text(f"dfs({v})", font_size=20))
        caja.move_to([PILA_X, PILA_Y0 + 0.42 * len(self.pila), 0])
        self.pila.append(caja)
        self.say(f"Entramos a {v}: tin[{v}] = low[{v}] = {ev['tin']}")
        self.s.play(self.g.N[v][0].animate.set_fill(C_ACTIVE, 1), FadeIn(self.lab[v]),
                    FadeIn(caja, shift=DOWN * 0.3), run_time=self.rt)

    def on_exit(self, ev):
        caja = self.pila.pop()
        self.s.play(self.g.N[ev["v"]][0].animate.set_fill(C_DONE, 1),
                    FadeOut(caja, shift=UP * 0.3), run_time=self.rt * 0.6)


class Demo(Scene):
    def construct(self):
        tj = load_trace("tarjan_demo")
        n, edges = tj["n"], tj["edges"]

        title = Text("Tarjan paso a paso", font_size=40).to_edge(UP, buff=0.3)
        sub = Text(f"Grafo de ejemplo: V = {n}, E = {len(edges)}  (traza real de bin/tarjan)",
                   font_size=22, color=GREY_A).next_to(title, DOWN, buff=0.12)
        g = GraphMob(n, edges, DEMO_POS)
        counter = Text("operaciones: 0", font_size=26, color=YELLOW).to_corner(UR)

        ley = VGroup(*[
            VGroup(Line(ORIGIN, RIGHT * 0.5).set_stroke(c, 6), Text(t, font_size=18)).arrange(RIGHT, buff=0.15)
            for c, t in [(C_TREE, "arista de árbol"), (C_BACK, "back edge"), (C_OK, "no es puente"), (C_BRIDGE, "puente")]
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.3, 2.05, 0])
        pila_t = Text("pila de recursión", font_size=20, color=GREY_A).move_to([PILA_X, PILA_Y0 - 0.5, 0])
        base = Line([PILA_X - 1.05, PILA_Y0 - 0.25, 0], [PILA_X + 1.05, PILA_Y0 - 0.25, 0]).set_stroke(GREY_B, 3)

        self.play(Write(title), FadeIn(sub))
        self.play(FadeIn(g), FadeIn(counter), FadeIn(ley), FadeIn(pila_t), Create(base))
        self.wait(0.8)

        player = TarjanConPila(self, g, rt=0.7, counter=counter)
        player.run(tj["events"])

        lista = ", ".join(f"e{i} ({edges[i][0]}–{edges[i][1]})" for i in tj["bridges"]) or "ninguno"
        player.say(f"Resultado: puentes = {lista}", C_BRIDGE)
        self.wait(2)

        # comprobacion visual: quitar los puentes deja componentes separadas
        player.say("Si quitamos los puentes, quedan bloques sin puentes (2-arista-conexos)", WHITE)
        anims = [g.E[e].animate.set_stroke(opacity=0.12) for e in tj["bridges"] if e in g.E]
        anims += [FadeOut(m) for m in player.lab.values()]
        self.play(*anims, run_time=1)
        padre = list(range(n))

        def find(x):
            while padre[x] != x:
                x = padre[x]
            return x

        for i, (u, v) in enumerate(edges):
            if i not in tj["bridges"]:
                padre[find(u)] = find(v)
        paleta = [TEAL_D, PURPLE_D, GOLD_D, MAROON_D]
        color = {}
        for v in range(n):
            if find(v) not in color:
                color[find(v)] = paleta[len(color) % len(paleta)]
        self.play(*[g.N[v][0].animate.set_fill(color[find(v)], 1) for v in range(n)])
        self.wait(1.5)

        comp = Text("Un solo DFS: cada nodo se visita una vez y cada arista se revisa dos veces  →  O(V + E)",
                    font_size=22, color=YELLOW).to_edge(DOWN, buff=1.1)
        self.play(FadeOut(pila_t), FadeOut(base), FadeIn(comp))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])
