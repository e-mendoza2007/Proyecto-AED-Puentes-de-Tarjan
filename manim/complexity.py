"""Parte B: comparación a ritmo narrable, consumiendo las trazas JSON reales de C++."""
import math
from common import *

POS = {0: (-4, 1), 1: (-2.5, 0), 2: (-4, -1), 3: (-0.8, 0),
       4: (0.5, 1), 5: (0.5, -1), 6: (1.9, -1), 7: (3.3, -1)}


class Complejidad(Scene):
    def clear_all(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

    def construct(self):
        tj, br = load_trace('tarjan_comparacion'), load_trace('brute_comparacion')
        scaling = load_trace('scaling')

        # 1) Los dos costes: dejar tiempo para LEER antes de pasar al grafo
        title = Text('¿Por qué conviene usar Tarjan?', font_size=40).to_edge(UP, buff=0.5)
        f1 = Text('Tarjan: O(V + E)', font_size=37, color=GREEN).move_to(UP * 0.65)
        w1 = Text('Un solo recorrido DFS', font_size=23, color=GREY_A).next_to(f1, DOWN, buff=0.22)
        f2 = Text('Fuerza bruta: O(E · (V + E))', font_size=34, color=RED).move_to(DOWN * 0.65)
        w2 = Text('Un BFS por cada arista retirada', font_size=23, color=GREY_A).next_to(f2, DOWN, buff=0.22)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(f1), FadeIn(w1), FadeIn(f2), FadeIn(w2), run_time=1.0)
        self.wait(4.0)
        self.clear_all()

        # 2) Tarjan: ejecución completa del mismo grafo de 8 nodos y 9 aristas
        g = GraphMob(tj['n'], tj['edges'], POS)
        head = Text('Tarjan: una única exploración DFS', font_size=31, color=GREEN).to_corner(UL)
        counter = Text('operaciones: 0', font_size=25, color=YELLOW).to_corner(UR)
        self.play(FadeIn(g), FadeIn(head), FadeIn(counter), run_time=0.8)
        TarjanPlayer(self, g, rt=0.23, counter=counter).run(tj['events'])
        self.wait(2.5)
        self.clear_all()

        # 3) Fuerza bruta: mismo grafo, todas las pruebas; ritmo más ágil entre visitas
        g = GraphMob(br['n'], br['edges'], POS)
        head = Text('Fuerza bruta: repetimos BFS por cada arista', font_size=29, color=RED).to_corner(UL)
        counter = Text('operaciones: 0', font_size=25, color=YELLOW).to_corner(UR)
        self.play(FadeIn(g), FadeIn(head), FadeIn(counter), run_time=0.8)
        BrutePlayer(self, g, rt=0.08, counter=counter).run(br['events'])
        self.wait(2.5)
        self.clear_all()

        # 4) Resultado exacto de las ejecuciones C++, no duración en segundos
        res = Text(f'Mismo grafo: {tj["n"]} vértices y {len(tj["edges"])} aristas',
                   font_size=33).shift(UP * 1.25)
        r1 = Text(f'Tarjan: {tj["ops"]} operaciones', font_size=37, color=GREEN)
        r2 = Text(f'Fuerza bruta: {br["ops"]} operaciones', font_size=37, color=RED)
        VGroup(r1, r2).arrange(DOWN, buff=0.45).next_to(res, DOWN, buff=0.6)
        self.play(Write(res), FadeIn(r1), FadeIn(r2), run_time=1.0)
        self.wait(5.0)
        self.clear_all()

        # 5) Escalamiento basado en scripts/make_scaling.py (eje Y logarítmico)
        ax = Axes(x_range=[0, 520, 100], y_range=[0, 7, 1], x_length=8.5,
                  y_length=4.3, tips=False).shift(DOWN * 0.3 + RIGHT * 0.5)
        ttl = Text('Operaciones al crecer el grafo (E ≈ 1.5 V)', font_size=28).to_edge(UP, buff=0.4)
        xl = Text('V (número de nodos)', font_size=20).next_to(ax, DOWN, buff=0.5)
        yl = Text('operaciones (escala log)', font_size=20).rotate(PI / 2).next_to(ax, LEFT, buff=0.9)
        ticks = VGroup(
            *[Text(f'1e{k}', font_size=16).next_to(ax.c2p(0, k), LEFT, buff=0.1) for k in range(8)],
            *[Text(str(x), font_size=16).next_to(ax.c2p(x, 0), DOWN, buff=0.1)
              for x in (0, 100, 200, 300, 400, 500)]
        )
        self.play(Write(ttl), Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), run_time=1.0)
        for key, col, name in (('tarjan_ops', GREEN, 'Tarjan'),
                               ('brute_ops', RED, 'Fuerza bruta')):
            pts = [ax.c2p(r['n'], math.log10(r[key])) for r in scaling]
            line = VMobject().set_points_as_corners(pts).set_stroke(col, 5)
            dots = VGroup(*[Dot(p, color=col, radius=0.06) for p in pts])
            lab = Text(name, font_size=24, color=col).next_to(
                pts[-1], LEFT if key == 'brute_ops' else UP, buff=0.2)
            self.play(Create(line), FadeIn(dots), FadeIn(lab), run_time=1.7)
        last = scaling[-1]
        foot = Text(f'Con V={last["n"]}: {last["tarjan_ops"]} vs {last["brute_ops"]} operaciones',
                    font_size=24).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(foot), run_time=0.7)
        self.wait(6.0)
