"""Parte B: casos borde narrables, con eventos REALES de fuerza bruta.

Cada caso visualiza una arista representativa retirándose, el BFS real y el resultado.
Las conclusiones se contrastan contra la traza de Tarjan generada por C++.
Render: python -m manim -pql manim/edge_cases.py CasoArbol CasoCiclo CasoParalelas CasoDesconectado
"""
from common import *
from fuerza_bruta import prueba_de_arista


class CasoBase(Scene):
    NAME, TITLE, SUB, RESULT = '', '', '', ''
    POS, SHOW_IDS, EDGE = {}, False, 0

    def construct(self):
        tj = load_trace(f'tarjan_{self.NAME}')
        br = load_trace(f'brute_{self.NAME}')
        if tj['bridges'] != br['bridges']:
            raise ValueError(f'Resultados distintos en el caso {self.NAME}')

        titulo = Text(self.TITLE, font_size=36).to_edge(UP, buff=0.35)
        subtitulo = Text(self.SUB, font_size=22, color=GREY_A).next_to(titulo, DOWN, buff=0.16)
        g = GraphMob(br['n'], br['edges'], self.POS, show_ids=self.SHOW_IDS)
        self.play(Write(titulo), FadeIn(subtitulo), run_time=1.0)
        self.play(FadeIn(g), run_time=1.0)
        self.wait(3.2)  # Voz: presentar el caso y su pregunta

        p = BrutePlayer(self, g, rt=0.36)
        p.run([br['events'][0]])  # Empieza indicando componentes originales
        bloque = prueba_de_arista(br['events'], self.EDGE)
        p.run(bloque[:-1])  # Quitar arista, BFS y comparar conectividad
        self.wait(2.5)      # Mostrar claramente el resultado antes de restaurar
        p.run(bloque[-1:])

        if self.NAME == 'disconnected':
            roots = [e['v'] for e in tj['events'] if e['t'] == 'new_root']
            p.say('Tarjan inicia DFS en cada componente: ' + ', '.join(map(str, roots)), YELLOW)
            for v in roots:
                self.play(Indicate(g.N[v], color=YELLOW), run_time=0.65)

        p.say(self.RESULT, GREEN_C)
        self.wait(4.0)  # Voz: cerrar con la regla general


class CasoArbol(CasoBase):
    NAME, TITLE = 'tree', 'Caso borde 1: un árbol'
    SUB = 'Sin ciclos: no existe ningún camino alternativo'
    RESULT = 'Todas sus aristas son puentes (Tarjan y fuerza bruta coinciden)'
    EDGE = 2  # Una arista representativa; src/brute.cpp comprueba las cinco.
    POS = {0: (0, 1.6), 1: (-2.4, 0), 2: (2.4, 0),
           3: (-3.6, -1.7), 4: (-1.2, -1.7), 5: (2.4, -1.7)}


class CasoCiclo(CasoBase):
    NAME, TITLE = 'cycle', 'Caso borde 2: un ciclo'
    SUB = 'Aunque quitemos una arista, existe otro camino'
    RESULT = 'Ninguna de sus aristas es puente (ambos métodos coinciden)'
    EDGE = 0
    POS = {0: (0, 1.9), 1: (1.8, 0.95), 2: (1.8, -0.95),
           3: (0, -1.9), 4: (-1.8, -0.95), 5: (-1.8, 0.95)}


class CasoParalelas(CasoBase):
    NAME, TITLE = 'parallel', 'Caso borde 3: aristas paralelas'
    SUB = 'e1 y e2 unen exactamente los mismos dos vértices'
    RESULT = 'e1 y e2 no son puentes; e0 y e3 sí lo son'
    EDGE = 1
    SHOW_IDS = True
    POS = {0: (-4.5, 0.2), 1: (-1.5, 0.2),
           2: (1.5, 0.2), 3: (4.5, 0.2)}


class CasoDesconectado(CasoBase):
    NAME, TITLE = 'disconnected', 'Caso borde 4: grafo desconectado'
    SUB = 'El grafo empieza con 3 componentes; también hay un nodo aislado'
    RESULT = 'Hay que explorar TODAS las componentes; puentes: e3, e4'
    EDGE = 3
    POS = {0: (-4.5, 0.9), 1: (-3.2, -0.9), 2: (-5.8, -0.9),
           3: (-0.5, 0.9), 4: (1.0, -0.9), 5: (2.5, 0.9), 6: (5.2, 0)}
