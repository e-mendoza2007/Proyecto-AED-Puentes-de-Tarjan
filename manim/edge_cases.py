"""Parte B - Casos borde. Uso: manim -qh manim/edge_cases.py CasoArbol CasoCiclo CasoParalelas CasoDesconectado"""
from common import *


class CasoBase(Scene):
    NAME, TITLE, SUB, NOTE = "", "", "", ""
    POS, SHOW_IDS = {}, False

    def construct(self):
        tj, br = load_trace(f"tarjan_{self.NAME}"), load_trace(f"brute_{self.NAME}")
        title = Text(self.TITLE, font_size=38).to_edge(UP, buff=0.4)
        sub = Text(self.SUB, font_size=22, color=GREY_A).next_to(title, DOWN, buff=0.15)
        g = GraphMob(tj["n"], tj["edges"], self.POS, show_ids=self.SHOW_IDS)
        counter = Text("operaciones: 0", font_size=26, color=YELLOW).to_corner(UR)
        self.play(Write(title), FadeIn(sub))
        self.play(FadeIn(g), FadeIn(counter))
        self.wait(0.5)

        player = TarjanPlayer(self, g, rt=0.45, counter=counter)
        player.run(tj["events"])

        ok = tj["bridges"] == br["bridges"]
        lista = ", ".join(f"e{i}" for i in tj["bridges"]) or "ninguno"
        player.say(f"Puentes: {lista}   |   fuerza bruta {'coincide' if ok else 'DIFIERE'}", GREEN if ok else RED)
        note = Text(self.NOTE, font_size=26, color=WHITE, line_spacing=0.8).to_edge(DOWN, buff=1.1)
        self.play(FadeIn(note))
        self.wait(3)


class CasoArbol(CasoBase):
    NAME, TITLE = "tree", "Caso borde 1: un árbol"
    SUB = "V nodos, V − 1 aristas, sin ciclos"
    NOTE = "En un árbol TODAS las aristas son puentes:\nninguna back edge permite 'subir'."
    POS = {0: (0, 1.6), 1: (-2.4, 0), 2: (2.4, 0), 3: (-3.6, -1.7), 4: (-1.2, -1.7), 5: (2.4, -1.7)}


class CasoCiclo(CasoBase):
    NAME, TITLE = "cycle", "Caso borde 2: un ciclo"
    SUB = "cada arista tiene un camino alterno"
    NOTE = "Una sola back edge hace que low[v] ≤ tin[u] en todo el ciclo:\nningún puente."
    POS = {0: (0, 1.9), 1: (1.8, 0.95), 2: (1.8, -0.95), 3: (0, -1.9), 4: (-1.8, -0.95), 5: (-1.8, 0.95)}


class CasoParalelas(CasoBase):
    NAME, TITLE = "parallel", "Caso borde 3: aristas paralelas"
    SUB = "dos aristas distintas (e1 y e2) entre los nodos 1 y 2"
    NOTE = "e1 y e2 NO son puentes: quitar una no desconecta.\nSe salta la arista padre por id, no por vértice."
    POS = {0: (-4.5, 0.2), 1: (-1.5, 0.2), 2: (1.5, 0.2), 3: (4.5, 0.2)}
    SHOW_IDS = True


class CasoDesconectado(CasoBase):
    NAME, TITLE = "disconnected", "Caso borde 4: grafo desconectado"
    SUB = "tres componentes: {0,1,2}, {3,4,5} y {6}"
    NOTE = "Un solo DFS no alcanza todos los nodos:\nse lanza uno desde cada nodo sin visitar."
    POS = {0: (-4.5, 0.9), 1: (-3.2, -0.9), 2: (-5.8, -0.9), 3: (-0.5, 0.9), 4: (1.0, -0.9), 5: (2.5, 0.9), 6: (5.2, 0)}
