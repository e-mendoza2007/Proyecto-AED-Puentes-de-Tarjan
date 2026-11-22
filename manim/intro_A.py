"""Parte A - Introduccion: que es un puente, para que sirve y como funciona Tarjan.
Uso: manim -qh manim/intro_A.py Intro
El puente del ejemplo NO esta puesto a mano: se obtiene corriendo bin/tarjan sobre graphs/intro.txt."""
import json
import subprocess

from common import *

INTRO_POS = {0: (-4.2, 1.0), 1: (-5.2, -0.8), 2: (-3.0, -0.8),
             3: (3.0, 1.0), 4: (2.0, -0.8), 5: (4.2, -0.8)}


def correr_tarjan(nombre):
    with open(ROOT / "graphs" / f"{nombre}.txt") as f:
        res = subprocess.run([str(ROOT / "bin" / "tarjan"), "--compact"], stdin=f,
                             capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def componentes(n, edges, quitada):
    padre = list(range(n))

    def find(x):
        while padre[x] != x:
            x = padre[x]
        return x

    for i, (u, v) in enumerate(edges):
        if i != quitada:
            padre[find(u)] = find(v)
    return [find(v) for v in range(n)]


class Intro(Scene):
    def construct(self):
        data = correr_tarjan("intro")
        n, edges, bridges = data["n"], data["edges"], data["bridges"]
        puente = bridges[0]
        otra = next(i for i in range(len(edges)) if i not in bridges)

        # 1) Que es un puente
        title = Text("¿Qué es un puente?", font_size=42).to_edge(UP, buff=0.4)
        self.play(Write(title))
        g = GraphMob(n, edges, INTRO_POS).shift(DOWN * 0.2)
        izq = Text("Ciudad A", font_size=24, color=GREY_A).move_to(LEFT * 4.1 + DOWN * 2.0)
        der = Text("Ciudad B", font_size=24, color=GREY_A).move_to(RIGHT * 3.1 + DOWN * 2.0)
        self.play(FadeIn(g), FadeIn(izq), FadeIn(der))
        cap = Text("Nodos = lugares, aristas = carreteras (o cables de red)", font_size=26).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(1.5)

        # quitar una arista que NO es puente
        new = Text("Si cortamos esta carretera... todavía hay otro camino", font_size=26).to_edge(DOWN, buff=0.4)
        self.play(g.E[otra].animate.set_stroke(C_EDGE, opacity=0.12), Transform(cap, new))
        self.wait(1.5)
        self.play(g.E[otra].animate.set_stroke(C_EDGE, opacity=1))

        # quitar el puente: se desconecta
        new = Text("Pero si cortamos ESTA, el grafo se parte en dos", font_size=26, color=C_BRIDGE).to_edge(DOWN, buff=0.4)
        self.play(g.E[puente].animate.set_stroke(C_BRIDGE, width=10), Transform(cap, new))
        self.wait(0.8)
        comp = componentes(n, edges, puente)
        colores = {}
        paleta = [TEAL_D, PURPLE_D, GOLD_D]
        anims = [g.E[puente].animate.set_stroke(opacity=0.12)]
        for v in range(n):
            if comp[v] not in colores:
                colores[comp[v]] = paleta[len(colores) % len(paleta)]
            anims.append(g.N[v][0].animate.set_fill(colores[comp[v]], 1))
        self.play(*anims)
        k = Text(f"Componentes conexas: 1 → {len(colores)}", font_size=28, color=YELLOW).next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(k))
        self.wait(1.5)

        defi = Text("Puente: arista cuya eliminación aumenta\nel número de componentes conexas",
                    font_size=30, line_spacing=0.9).to_edge(DOWN, buff=0.35)
        self.play(Transform(cap, defi))
        self.wait(2.5)
        self.play(FadeOut(VGroup(g, izq, der, k, cap, title)))

        # 2) Para que sirve
        title = Text("¿Para qué sirve?", font_size=42).to_edge(UP, buff=0.4)
        usos = VGroup(
            Text("• Redes de computadoras: detectar el cable cuya caída aísla equipos", font_size=26),
            Text("• Carreteras y redes eléctricas: encontrar puntos únicos de falla", font_size=26),
            Text("• Base de otros algoritmos: componentes 2-arista-conexas", font_size=26),
            Text("Es un ALGORITMO (no un TDA): trabaja sobre un grafo no dirigido", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        self.play(Write(title))
        for u in usos:
            self.play(FadeIn(u, shift=RIGHT * 0.3), run_time=0.7)
            self.wait(0.8)
        self.wait(1.5)
        self.play(FadeOut(usos), FadeOut(title))

        # 3) Como funciona
        title = Text("¿Cómo funciona? Tarjan: un solo DFS", font_size=40).to_edge(UP, buff=0.4)
        self.play(Write(title))
        ideas = VGroup(
            Text("tin[v]: momento en que el DFS descubre a v", font_size=26),
            Text("low[v]: el menor tin al que puede volver el subárbol de v\n          usando a lo más una back edge", font_size=26, line_spacing=0.8),
            Text("La arista de árbol (u, v) es PUENTE  ⇔  low[v] > tin[u]", font_size=28, color=C_BRIDGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP * 1.2)
        for t in ideas:
            self.play(FadeIn(t), run_time=0.7)
            self.wait(1.2)

        # dibujo: subarbol de v que no puede volver por encima de u
        u = VGroup(Circle(0.28).set_fill(C_NODE, 1).set_stroke(WHITE, 3), Text("u", font_size=24)).move_to(LEFT * 5 + DOWN * 1.2)
        v = VGroup(Circle(0.28).set_fill(C_NODE, 1).set_stroke(WHITE, 3), Text("v", font_size=24)).move_to(LEFT * 5 + DOWN * 2.4)
        tri = Polygon(LEFT * 5 + DOWN * 2.7, LEFT * 5.9 + DOWN * 3.6, LEFT * 4.1 + DOWN * 3.6).set_stroke(GREY_B, 2)
        e = Line(u.get_bottom(), v.get_top()).set_stroke(C_BRIDGE, 8)
        lab = Text("PUENTE: ninguna back edge\ndel subárbol llega a u o arriba", font_size=20, color=C_BRIDGE, line_spacing=0.8).next_to(tri, RIGHT, buff=0.3)
        u2 = u.copy().move_to(RIGHT * 0.8 + DOWN * 1.2)
        v2 = v.copy().move_to(RIGHT * 0.8 + DOWN * 2.4)
        tri2 = tri.copy().move_to(RIGHT * 0.8 + DOWN * 3.15)
        e2 = Line(u2.get_bottom(), v2.get_top()).set_stroke(C_OK, 8)
        back = CurvedArrow(tri2.get_corner(DR) + UP * 0.1, u2.get_right(), angle=PI / 2.2, color=C_BACK)
        lab2 = Text("NO es puente: una back edge\nllega a u o más arriba", font_size=20, color=C_BACK, line_spacing=0.8).next_to(tri2, RIGHT, buff=0.7)
        self.play(FadeIn(u, v, tri), Create(e), FadeIn(lab))
        self.play(FadeIn(u2, v2, tri2), Create(e2), Create(back), FadeIn(lab2))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])
