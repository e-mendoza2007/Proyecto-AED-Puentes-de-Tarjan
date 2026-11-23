"""Parte B: dos pruebas de fuerza bruta con eventos VERDADEROS de src/brute.cpp.

Render: python -m manim -pql manim/fuerza_bruta.py FuerzaBruta
Narrar siguiendo GUIÓN_B_SINCRONIZADO.md. Esta escena no calcula resultados a mano.
"""
from common import *

POS = {0: (-4.3, 0.2), 1: (-1.45, 0.2), 2: (1.45, 0.2), 3: (4.3, 0.2)}


def prueba_de_arista(events, edge_id):
    """Extrae los eventos emitidos por C++ desde remove(e) hasta restore(e).

    Conserva su orden y sus contadores 'ops' originales.
    """
    start = next(i for i, e in enumerate(events)
                 if e['t'] == 'remove' and e['e'] == edge_id)
    end = next(i for i in range(start, len(events))
               if events[i]['t'] == 'restore' and events[i]['e'] == edge_id)
    return events[start:end + 1]


class FuerzaBruta(Scene):
    def construct(self):
        trace = load_trace('brute_parallel')
        titulo = Text('¿Cómo sabemos si una arista es puente?', font_size=35).to_edge(UP, buff=0.35)
        subtitulo = Text('Quitamos una arista y contamos las componentes conexas',
                         font_size=23, color=GREY_A).next_to(titulo, DOWN, buff=0.14)
        g = GraphMob(trace['n'], trace['edges'], POS, show_ids=True)
        self.play(Write(titulo), FadeIn(subtitulo), run_time=1.0)
        self.play(FadeIn(g), run_time=1.0)
        self.wait(5.5)  # Voz: planteamiento del método

        p = BrutePlayer(self, g, rt=0.50)
        p.run([trace['events'][0]])  # Componentes iniciales: 1, emitido por C++.
        self.wait(2.0)  # Explicar qué significa componente conexa

        for e, etiqueta in ((0, 'Primera prueba: quitamos e0'),
                            (1, 'Segunda prueba: quitamos e1')):
            linea = Text(etiqueta, font_size=27, color=YELLOW).move_to(UP * 2.0)
            self.play(FadeIn(linea), run_time=0.6)
            bloque = prueba_de_arista(trace['events'], e)
            # Pausa DURANTE el veredicto, antes de restaurar, para poder explicarlo.
            p.run(bloque[:-1])
            self.wait(5.0)
            p.run(bloque[-1:])
            self.play(FadeOut(linea), run_time=0.35)

        p.say('Repetimos la misma prueba para CADA arista del grafo', GREEN_C)
        self.wait(4.7)
