"""Parte B - Complejidad. Uso: manim -qh manim/complexity.py Complejidad"""
import math
from common import *

POS = {0: (-4, 1), 1: (-2.5, 0), 2: (-4, -1), 3: (-0.8, 0), 4: (0.5, 1), 5: (0.5, -1), 6: (1.9, -1), 7: (3.3, -1)}


class Complejidad(Scene):
    def clear_all(self):
        self.play(*[FadeOut(m) for m in self.mobjects])

    def construct(self):
        tj, br = load_trace("tarjan_comparacion"), load_trace("brute_comparacion")
        scaling = load_trace("scaling")

        # 1) Las dos cotas
        title = Text("Complejidad: Tarjan vs fuerza bruta", font_size=40).to_edge(UP, buff=0.5)
        f1 = Text("Tarjan:  O(V + E)", font_size=36, color=GREEN)
        f2 = Text("Fuerza bruta:  O(E · (V + E))", font_size=36, color=RED)
        VGroup(f1, f2).arrange(DOWN, buff=0.6)
        why1 = Text("cada nodo y cada arista se visitan una vez", font_size=22, color=GREY_A).next_to(f1, RIGHT, buff=0.5)
        why2 = Text("E aristas × un BFS de O(V + E)", font_size=22, color=GREY_A).next_to(f2, RIGHT, buff=0.5)
        VGroup(f1, why1).move_to(UP * 0.6 + LEFT * 0.0)
        self.play(Write(title))
        self.play(FadeIn(f1), FadeIn(why1))
        self.play(FadeIn(f2.next_to(f1, DOWN, buff=0.7).align_to(f1, LEFT)), FadeIn(why2.next_to(f2, RIGHT, buff=0.5)))
        self.wait(2)
        self.clear_all()

        # 2) Corrida corta de Tarjan
        g = GraphMob(tj["n"], tj["edges"], POS)
        head = Text("Tarjan  ·  O(V + E)", font_size=32, color=GREEN).to_corner(UL)
        counter = Text("operaciones: 0", font_size=26, color=YELLOW).to_corner(UR)
        self.play(FadeIn(g), FadeIn(head), FadeIn(counter))
        TarjanPlayer(self, g, rt=0.3, counter=counter).run(tj["events"])
        self.wait(1.5)
        self.clear_all()

        # 3) Corrida corta de la fuerza bruta (mismo grafo)
        g = GraphMob(br["n"], br["edges"], POS)
        head = Text("Fuerza bruta  ·  O(E · (V + E))", font_size=32, color=RED).to_corner(UL)
        counter = Text("operaciones: 0", font_size=26, color=YELLOW).to_corner(UR)
        self.play(FadeIn(g), FadeIn(head), FadeIn(counter))
        BrutePlayer(self, g, rt=0.12, counter=counter).run(br["events"])
        self.wait(1.5)
        self.clear_all()

        # 4) Mismo grafo: cuantas operaciones
        m = len(tj["edges"])
        res = Text(f"Mismo grafo (V = {tj['n']}, E = {m})", font_size=34).shift(UP * 1.2)
        r1 = Text(f"Tarjan: {tj['ops']} operaciones", font_size=36, color=GREEN)
        r2 = Text(f"Fuerza bruta: {br['ops']} operaciones", font_size=36, color=RED)
        VGroup(r1, r2).arrange(DOWN, buff=0.4).next_to(res, DOWN, buff=0.6)
        self.play(Write(res), FadeIn(r1), FadeIn(r2))
        self.wait(2.5)
        self.clear_all()

        # 5) Crecimiento al aumentar n (escala logaritmica en y)
        ax = Axes(x_range=[0, 520, 100], y_range=[0, 7, 1], x_length=8.5, y_length=4.3, tips=False).shift(DOWN * 0.3 + RIGHT * 0.5)
        ttl = Text("Operaciones según el tamaño del grafo (E ≈ 1.5 V)", font_size=28).to_edge(UP, buff=0.4)
        xl = Text("V (número de nodos)", font_size=20).next_to(ax, DOWN, buff=0.5)
        yl = Text("operaciones (escala log)", font_size=20).rotate(PI / 2).next_to(ax, LEFT, buff=0.9)
        ticks = VGroup(*[Text(f"1e{k}", font_size=16).next_to(ax.c2p(0, k), LEFT, buff=0.1) for k in range(8)],
                       *[Text(str(x), font_size=16).next_to(ax.c2p(x, 0), DOWN, buff=0.1) for x in (0, 100, 200, 300, 400, 500)])
        self.play(Write(ttl), Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl))
        for key, col, name in (("tarjan_ops", GREEN, "Tarjan"), ("brute_ops", RED, "Fuerza bruta")):
            pts = [ax.c2p(r["n"], math.log10(r[key])) for r in scaling]
            line = VMobject().set_points_as_corners(pts).set_stroke(col, 5)
            dots = VGroup(*[Dot(p, color=col, radius=0.06) for p in pts])
            lab = Text(name, font_size=24, color=col).next_to(pts[-1], LEFT if key == "brute_ops" else UP, buff=0.2)
            self.play(Create(line), FadeIn(dots), FadeIn(lab), run_time=2)
        last = scaling[-1]
        foot = Text(f"Con V = {last['n']}: {last['tarjan_ops']} vs {last['brute_ops']} operaciones", font_size=24).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(foot))
        self.wait(3)
