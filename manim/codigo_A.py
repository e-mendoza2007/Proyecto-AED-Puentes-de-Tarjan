"""Parte A - El codigo real de dfs (leido de src/tarjan.cpp) con las lineas clave resaltadas.
Uso: manim -qh manim/codigo_A.py Codigo
Se quitan solo las llamadas a evento(...), que sirven para generar la traza de la animacion."""
from common import *


def leer_dfs():
    lineas = (ROOT / "src" / "tarjan.cpp").read_text().splitlines()
    ini = next(i for i, l in enumerate(lineas) if l.startswith("void dfs"))
    res, saltando = [], False
    for l in lineas[ini:]:
        if "evento(" in l:
            saltando = True
        if saltando:
            if l.rstrip().endswith(");"):
                saltando = False
            continue
        if l.strip() == "" or l.strip() == "ops++;":
            continue
        res.append(l)
        if l == "}":
            break
    return res


PASOS = [
    ("tin[u] = timer_;", "Al entrar a u:\ntin[u] = low[u] = timer"),
    ("aristaPadre) continue", "Saltamos la arista padre por su id,\nasí las aristas paralelas funcionan"),
    ("low[u] = min(low[u], tin[v])", "v ya visitado y más arriba:\nback edge, low[u] baja a tin[v]"),
    ("dfs(v, id);", "v sin visitar: arista de árbol,\nbajamos con la recursión"),
    ("low[u] = min(low[u], low[v])", "Al volver, u hereda el low\ndel hijo"),
    ("bool puente", "Criterio: si low[v] > tin[u],\nla arista (u, v) es puente"),
]


class Codigo(Scene):
    def construct(self):
        lineas = leer_dfs()
        title = Text("El código: src/tarjan.cpp", font_size=38).to_edge(UP, buff=0.3)
        code = Code(code_string="\n".join(lineas), language="cpp", background="window",
                    formatter_style="monokai", add_line_numbers=False)
        code.scale_to_fit_height(6.0)
        if code.width > 7.6:
            code.scale_to_fit_width(7.6)
        code.to_edge(LEFT, buff=0.4).shift(DOWN * 0.35)
        self.play(Write(title), FadeIn(code))
        nota = Text("(sin las líneas de la traza\nni el contador de operaciones)", font_size=20, color=GREY_A,
                    line_spacing=0.8).move_to([3.9, 2.2, 0])
        self.play(FadeIn(nota))
        self.wait(1)

        caja, texto = None, None
        for clave, explicacion in PASOS:
            i = next(k for k, l in enumerate(lineas) if clave in l)
            if clave == "tin[u] = timer_;":
                grupo = VGroup(*code.code_lines[i:i + 3])
            else:
                grupo = code.code_lines[i]
            nueva = SurroundingRectangle(grupo, color=YELLOW, buff=0.06)
            nuevo_t = Text(explicacion, font_size=26, line_spacing=0.9,
                           color=C_BRIDGE if clave == "bool puente" else WHITE).move_to([3.9, 0, 0])
            if caja is None:
                self.play(Create(nueva), FadeIn(nuevo_t))
            else:
                self.play(Transform(caja, nueva), FadeOut(texto), FadeIn(nuevo_t))
                nueva = caja
            caja, texto = nueva, nuevo_t
            self.wait(2.6)

        fin = Text("En main se llama a dfs\ndesde cada nodo sin visitar\n(grafos desconectados)",
                   font_size=24, line_spacing=0.9).move_to([3.9, 0, 0])
        self.play(FadeOut(caja), FadeOut(texto), FadeIn(fin))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])
