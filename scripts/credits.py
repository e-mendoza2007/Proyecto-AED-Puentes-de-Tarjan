"""Portada y creditos (requisito: titulo del proyecto y nombres de los integrantes).
Uso: manim -qh manim/credits.py Portada Creditos"""
from common import *

TITULO = "Puentes en un grafo: algoritmo de Tarjan"
CURSO = "CS2023 - Algoritmos y Estructuras de Datos  |  UTEC 2026-2"
INTEGRANTES = ["Mahir Gianpier Gutierrez Rodriguez", "Ernesto Yen Mendoza Aguilar"]
INSPIRACION = "Estilo inspirado en 3Blue1Brown y la galeria de Manim Community"


class Portada(Scene):
    def construct(self):
        t = Text(TITULO, font_size=44).shift(UP * 1.2)
        c = Text(CURSO, font_size=24, color=GREY_A).next_to(t, DOWN, buff=0.4)
        n = VGroup(*[Text(x, font_size=28) for x in INTEGRANTES]).arrange(DOWN, buff=0.25).next_to(c, DOWN, buff=0.8)
        self.play(Write(t)); self.play(FadeIn(c)); self.play(FadeIn(n)); self.wait(2)


class Creditos(Scene):
    def construct(self):
        t = Text("Creditos", font_size=44).to_edge(UP)
        n = VGroup(*[Text(x, font_size=30) for x in INTEGRANTES]).arrange(DOWN, buff=0.3)
        r = Text("Codigo: C++17 + Manim Community  |  github.com/e-mendoza2007/Proyecto-AED-Puentes-de-Tarjan", font_size=22, color=GREY_A).to_edge(DOWN, buff=1.0)
        i = Text(INSPIRACION, font_size=20, color=GREY_B).to_edge(DOWN, buff=0.4)
        self.play(Write(t), FadeIn(n)); self.play(FadeIn(r), FadeIn(i)); self.wait(3)
