"""Diagrama de interacción P-M de columna de hormigón armado — ACI 318-19."""

from smathpy import (
    Worksheet, TextRegion, MathRegion, PlotRegion,
    var, assign, evaluate, num, func_assign, call,
)
from smathpy.expression import (
    sum_, if_, line, for_loop, range_,
    mat, el, col, stack, cinterp, augment,
)
from smathpy.expression.functions import sqrt, max_, min_, abs_, sign
from smathpy.units import (
    with_unit, compound_unit, value_with_compound_unit, power_unit,
)


def main() -> None:
    ws = Worksheet(title="Diagrama de Interacción — Columna HA ACI 318-19",
                   author="FCB")

    # ════════════════════════════════════════════════════════════════════
    # TÍTULO
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.title(
        "Diagrama de Interacción P-M — Columna de Hormigón Armado — ACI 318-19"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 1. GEOMETRÍA
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("1. Geometría de la sección"))

    ws.add(MathRegion.assignment("b", 400, unit_name="mm",
                                 description="Ancho de la columna"))
    ws.add(MathRegion.assignment("h", 400, unit_name="mm",
                                 description="Altura de la columna (dirección de flexión)"))
    ws.add(MathRegion.assignment("r", 40, unit_name="mm",
                                 description="Recubrimiento libre"))

    # ════════════════════════════════════════════════════════════════════
    # 2. MATERIALES
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("2. Propiedades de los materiales"))

    ws.add(MathRegion.assignment("f'_c", 28, unit_name="MPa",
                                 description="Resistencia a compresión del hormigón"))
    ws.add(MathRegion.assignment("f_y", 420, unit_name="MPa",
                                 description="Fluencia del acero"))
    ws.add(MathRegion.assignment("E_s", 200000, unit_name="MPa",
                                 description="Módulo de elasticidad del acero"))

    # β₁ según f'c — ACI 318-19 §22.2.2.4.3
    f_c = var("f'_c")
    beta1_expr = if_(
        f_c <= (num(28) @ "MPa"),
        num(0.85),
        if_(
            f_c >= (num(56) @ "MPa"),
            num(0.65),
            num(0.85) - num(0.05) * (f_c - (num(28) @ "MPa")) / (num(7) @ "MPa")
        )
    )
    ws.add(MathRegion(
        expr=assign("β_1", beta1_expr),
        show_result=True,
        description="Factor del bloque de compresión — ACI 22.2.2.4.3"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 3. ARMADURA LONGITUDINAL
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("3. Armadura longitudinal"))

    ws.add(MathRegion.assignment("N_x", 3,
                                 description="Barras por cara perpendicular al eje de flexión"))
    ws.add(MathRegion.assignment("N_y", 3,
                                 description="Barras por cara paralela al eje de flexión (capas)"))
    ws.add(MathRegion.assignment("d_b", 22, unit_name="mm",
                                 description="Diámetro de barras longitudinales"))
    ws.add(MathRegion.assignment("d_e", 10, unit_name="mm",
                                 description="Diámetro del estribo"))

    # Propiedades calculadas
    pi = var("π")
    d_b = var("d_b")
    d_e = var("d_e")
    N_x = var("N_x")
    N_y = var("N_y")

    # A_b = π/4 · d_b²
    A_b_expr = pi / num(4) * d_b ** num(2)
    ws.add(MathRegion(
        expr=assign("A_b", A_b_expr),
        show_result=True,
        contract_expr=power_unit("mm", 2),
        description="Área de una barra"
    ))

    # N_total = 2·N_x + 2·(N_y - 2)
    N_total_expr = num(2) * N_x + num(2) * (N_y - num(2))
    ws.add(MathRegion(
        expr=assign("N_total", N_total_expr),
        show_result=True,
        description="Número total de barras"
    ))

    # A_s.total = N_total · A_b
    A_s_total_expr = var("N_total") * var("A_b")
    ws.add(MathRegion(
        expr=assign("A_s.total", A_s_total_expr),
        show_result=True,
        contract_expr=power_unit("mm", 2),
        description="Área total de acero longitudinal"
    ))
    ws.add_spacing(10)

    # Cuantía geométrica: ρ_g = A_s.total / (b·h)
    b = var("b")
    h = var("h")
    rho_g_expr = var("A_s.total") / (b * h)
    ws.add(MathRegion(
        expr=assign("ρ_g", rho_g_expr),
        show_result=True,
        description="Cuantía geométrica"
    ))

    # Verificación 1% ≤ ρ_g ≤ 8% — ACI 10.6.1.1 (informativa)
    ws.add(MathRegion(
        expr=evaluate("ρ_g"),
        show_result=True,
        description="Verificar: 0.01 ≤ ρ_g ≤ 0.08 — ACI 10.6.1.1"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 4. SOLICITACIONES DE DISEÑO
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("4. Solicitaciones de diseño (punto a verificar)"))

    ws.add(MathRegion(
        expr=assign("P_u", num(1500) @ "kN"),
        description="Carga axial última de diseño"
    ))
    ws.add(MathRegion(
        expr=assign("M_u", value_with_compound_unit(120, ["kN", "m"], [])),
        description="Momento último de diseño"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 5. PROPIEDADES CALCULADAS
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("5. Propiedades de la sección"))

    r = var("r")

    # d' = r + d_e + d_b/2 — distancia al centroide de la primera capa
    dprime_expr = r + d_e + d_b / num(2)
    ws.add(MathRegion(
        expr=assign("d'", dprime_expr),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Distancia al centroide de la capa extrema"
    ))

    # d_t = h - d' — altura efectiva
    dprime = var("d'")
    dt_expr = h - dprime
    ws.add(MathRegion(
        expr=assign("d_t", dt_expr),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Altura efectiva (capa extrema de tracción)"
    ))

    # n_layers = N_y — número de capas
    ws.add(MathRegion(
        expr=assign("n_layers", N_y),
        show_result=True,
        description="Número de capas de armadura"
    ))

    # ε_cu = 0.003 — deformación última del hormigón
    ws.add(MathRegion.assignment("ε_cu", 0.003,
                                 description="Deformación última del hormigón — ACI 22.2.2.1"))

    # ε_y = f_y / E_s
    f_y = var("f_y")
    E_s = var("E_s")
    ws.add(MathRegion(
        expr=assign("ε_y", f_y / E_s),
        show_result=True,
        description="Deformación de fluencia del acero"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 6. MODELO DE ARMADURA POR CAPAS
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("6. Modelo de armadura por capas"))

    n_layers = var("n_layers")
    A_b = var("A_b")
    d_t = var("d_t")
    i = var("i")

    # d_layer(i) = d' + (i - 1)·(d_t - d') / (n_layers - 1)
    d_layer_body = dprime + (i - num(1)) * (d_t - dprime) / (n_layers - num(1))
    ws.add(MathRegion(
        expr=func_assign("d_layer", ["i"], d_layer_body),
        description="Posición de la capa i desde la fibra de compresión extrema"
    ))

    # A_layer(i): área de acero en la capa i
    # Capas extremas (i=1, i=n_layers): N_x barras
    # Capas intermedias: 2 barras (solo las de las caras laterales)
    A_layer_body = if_(
        i.eq(num(1)),
        N_x * A_b,
        if_(
            i.eq(n_layers),
            N_x * A_b,
            num(2) * A_b
        )
    )
    ws.add(MathRegion(
        expr=func_assign("A_layer", ["i"], A_layer_body),
        description="Área de acero en la capa i"
    ))

    # Verificación: mostrar d_layer y A_layer para cada capa
    ws.add(MathRegion(
        expr=assign("d_layers",
                     mat([[call("d_layer", num(j))] for j in range(1, 4)])),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Posiciones de las capas (verificación para N_y=3)"
    ))
    ws.add_spacing(10)
    ws.add(MathRegion(
        expr=assign("A_layers",
                     mat([[call("A_layer", num(j))] for j in range(1, 4)])),
        show_result=True,
        contract_expr=power_unit("mm", 2),
        description="Áreas por capa (verificación para N_y=3)"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 7. COMPATIBILIDAD DE DEFORMACIONES Y TENSIONES
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("7. Compatibilidad de deformaciones — ACI 22.2.2"))

    c_var = var("c")
    eps_cu = var("ε_cu")

    # ε_s(c, i) = ε_cu · (c - d_layer(i)) / c
    eps_s_body = eps_cu * (c_var - call("d_layer", i)) / c_var
    ws.add(MathRegion(
        expr=func_assign("ε_s", ["c", "i"], eps_s_body),
        description="Deformación en la capa i para profundidad del eje neutro c"
    ))

    # f_s(c, i) = min(|E_s · ε_s(c,i)|, f_y) · sign(ε_s(c,i))
    eps_s_ci = call("ε_s", c_var, i)
    fs_body = min_(mat([
        [abs_(E_s * eps_s_ci)],
        [f_y]
    ])) * sign(eps_s_ci)
    ws.add(MathRegion(
        expr=func_assign("f_s", ["c", "i"], fs_body),
        description="Tensión en el acero de la capa i (acotada a ±f_y)"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 8. FUERZAS Y RESISTENCIA NOMINAL
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("8. Resistencia nominal — ACI 22.4"))

    beta1 = var("β_1")
    f_s_ci = call("f_s", c_var, i)
    d_layer_i = call("d_layer", i)
    A_layer_i = call("A_layer", i)

    # F_bar(c, i): fuerza neta en la capa i, descontando concreto desplazado
    # si la barra está dentro del bloque de compresión (d_layer(i) ≤ β₁·c)
    F_bar_body = if_(
        d_layer_i <= beta1 * c_var,
        (f_s_ci - num(0.85) * f_c) * A_layer_i,
        f_s_ci * A_layer_i
    )
    ws.add(MathRegion(
        expr=func_assign("F_bar", ["c", "i"], F_bar_body),
        description="Fuerza neta en la capa i (descontando concreto desplazado)"
    ))

    # a(c) = min(β₁·c, h) — profundidad del bloque de compresión
    a_body = min_(mat([[beta1 * c_var], [h]]))
    ws.add(MathRegion(
        expr=func_assign("a", ["c"], a_body),
        description="Profundidad del bloque de compresión equivalente"
    ))

    # C_c(c) = 0.85 · f'c · a(c) · b — fuerza de compresión del concreto
    Cc_body = num(0.85) * f_c * call("a", c_var) * b
    ws.add(MathRegion(
        expr=func_assign("C_c", ["c"], Cc_body),
        description="Fuerza de compresión del bloque de hormigón"
    ))
    ws.add_spacing(10)

    # P_n(c) = C_c(c) + Σ F_bar(c, k) para k = 1..n_layers
    k = var("k")
    Pn_body = call("C_c", c_var) + sum_(
        call("F_bar", c_var, k), "k", num(1), n_layers
    )
    ws.add(MathRegion(
        expr=func_assign("P_n", ["c"], Pn_body),
        description="Carga axial nominal — positiva = compresión"
    ))

    # M_n(c) = C_c(c)·(h/2 - a(c)/2)
    #        + Σ F_bar(c,k)·(h/2 - d_layer(k)) para k = 1..n_layers
    Mn_body = (
        call("C_c", c_var) * (h / num(2) - call("a", c_var) / num(2))
        + sum_(
            call("F_bar", c_var, k) * (h / num(2) - call("d_layer", k)),
            "k", num(1), n_layers
        )
    )
    ws.add(MathRegion(
        expr=func_assign("M_n", ["c"], Mn_body),
        description="Momento nominal respecto al centroide geométrico"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 9. FACTOR DE REDUCCIÓN φ — ACI 318-19 §21.2
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("9. Factor φ — ACI 318-19 Tabla 21.2.2"))

    eps_y = var("ε_y")

    # ε_t(c) = ε_cu · (d_t - c) / c — deformación en la capa extrema de tracción
    eps_t_body = eps_cu * (d_t - c_var) / c_var
    ws.add(MathRegion(
        expr=func_assign("ε_t", ["c"], eps_t_body),
        description="Deformación en la capa extrema de tracción"
    ))

    eps_t_c = call("ε_t", c_var)

    # φ(c): columnas con estribos — Tabla 21.2.2
    # ε_t ≥ ε_y + 0.003  →  φ = 0.90  (controlada por tracción)
    # ε_t ≤ ε_y          →  φ = 0.65  (controlada por compresión)
    # transición          →  φ = 0.65 + 0.25·(ε_t - ε_y) / 0.003
    phi_body = if_(
        eps_t_c >= eps_y + num(0.003),
        num(0.90),
        if_(
            eps_t_c <= eps_y,
            num(0.65),
            num(0.65) + num(0.25) * (eps_t_c - eps_y) / num(0.003)
        )
    )
    ws.add(MathRegion(
        expr=func_assign("φ", ["c"], phi_body),
        description="Factor de reducción φ para columnas con estribos"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 10. PUNTOS NOTABLES
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("10. Puntos notables del diagrama"))

    A_s_total = var("A_s.total")

    # ── Compresión pura ──
    # P_0 = 0.85·f'c·(b·h - A_s.total) + f_y·A_s.total
    P0_expr = num(0.85) * f_c * (b * h - A_s_total) + f_y * A_s_total
    ws.add(MathRegion(
        expr=assign("P_0", P0_expr),
        show_result=True,
        contract_expr=compound_unit(["kN"], []),
        description="Resistencia nominal a compresión pura"
    ))
    ws.add_spacing(10)

    # P_0.max = 0.80·P_0 — ACI Tabla 22.4.2.1 (estribos)
    P0_max_expr = num(0.80) * var("P_0")
    ws.add(MathRegion(
        expr=assign("P_0.max", P0_max_expr),
        show_result=True,
        contract_expr=compound_unit(["kN"], []),
        description="Capacidad máxima a compresión — ACI Tabla 22.4.2.1"
    ))

    # ── Tracción pura ──
    Pt_expr = -f_y * A_s_total
    ws.add(MathRegion(
        expr=assign("P_t", Pt_expr),
        show_result=True,
        contract_expr=compound_unit(["kN"], []),
        description="Resistencia nominal a tracción pura"
    ))

    # ── Punto balanceado ──
    # c_b = ε_cu · d_t / (ε_cu + ε_y)
    cb_expr = eps_cu * d_t / (eps_cu + eps_y)
    ws.add(MathRegion(
        expr=assign("c_b", cb_expr),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Profundidad del eje neutro en punto balanceado"
    ))
    ws.add_spacing(10)

    c_b = var("c_b")
    ws.add(MathRegion(
        expr=assign("P_b", call("P_n", c_b)),
        show_result=True,
        contract_expr=compound_unit(["kN"], []),
        description="Carga axial en punto balanceado"
    ))
    ws.add(MathRegion(
        expr=assign("M_b", call("M_n", c_b)),
        show_result=True,
        contract_expr=compound_unit(["kN", "m"], []),
        description="Momento en punto balanceado"
    ))

    # ── Flexión pura ──
    # Buscar c tal que P_n(c) = 0 usando solve de SMath
    # solve(P_n(c_0), c_0, d_t/2) — estimación inicial d_t/2
    c_0_expr = call("solve", call("P_n", var("c_0")), var("c_0"), d_t / num(2))
    ws.add(MathRegion(
        expr=assign("c_fp", c_0_expr),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Profundidad del eje neutro en flexión pura (P_n = 0)"
    ))
    ws.add_spacing(10)

    c_fp = var("c_fp")
    ws.add(MathRegion(
        expr=assign("M_0", call("M_n", c_fp)),
        show_result=True,
        contract_expr=compound_unit(["kN", "m"], []),
        description="Momento nominal en flexión pura"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 11. GENERACIÓN DE LA CURVA DE INTERACCIÓN
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("11. Generación de la curva P-M"))

    # Número de puntos para la curva
    ws.add(MathRegion.assignment("n_pts", 50,
                                 description="Número de puntos de la curva"))
    n_pts = var("n_pts")

    # Rango de c: de un valor pequeño (d_b) hasta un valor grande (5·h)
    # para barrer desde tracción pura hasta compresión pura
    ws.add(MathRegion(
        expr=assign("c_min", d_b),
        description="Profundidad mínima del eje neutro"
    ))
    ws.add(MathRegion(
        expr=assign("c_max", num(5) * h),
        description="Profundidad máxima del eje neutro"
    ))
    ws.add_spacing(10)

    c_min = var("c_min")
    c_max = var("c_max")

    # Δc = (c_max - c_min) / (n_pts - 1)
    ws.add(MathRegion(
        expr=assign("Δc", (c_max - c_min) / (n_pts - num(1))),
        description="Incremento de c"
    ))

    dc = var("Δc")

    # c_k(j) = c_min + (j - 1)·Δc
    ws.add(MathRegion(
        expr=func_assign("c_k", ["j"], c_min + (var("j") - num(1)) * dc),
        description="Valor de c para el punto j"
    ))

    # ── Construir matriz de resultados con for_loop ──
    # Columnas: [M_n, P_n, φ·M_n, φ·P_n]
    # Inicializar con primera fila
    j = var("j")
    P0_var = var("P_0")
    P0_max_var = var("P_0.max")

    # Fila inicial (j=1): primera iteración
    c_1 = call("c_k", num(1))
    Pn_1 = call("P_n", c_1)
    Mn_1 = call("M_n", c_1)
    phi_1 = call("φ", c_1)

    # Capacidad de compresión limitada a P_0.max (0.80·P_0)
    Pn_capped_1 = min_(mat([[Pn_1], [P0_max_var]]))
    phi_Pn_1 = min_(mat([[phi_1 * Pn_1], [num(0.65) * P0_max_var]]))

    init_row = mat([[Mn_1, Pn_capped_1, phi_1 * Mn_1, phi_Pn_1]])

    ws.add(MathRegion(
        expr=assign("Res", init_row),
        description="Fila inicial de resultados"
    ))

    Res = var("Res")

    # Cuerpo del for_loop
    c_j = call("c_k", j)
    Pn_j = call("P_n", c_j)
    Mn_j = call("M_n", c_j)
    phi_j = call("φ", c_j)
    Pn_capped = min_(mat([[Pn_j], [P0_max_var]]))
    phi_Pn_j = min_(mat([[phi_j * Pn_j], [num(0.65) * P0_max_var]]))

    new_row = mat([[Mn_j, Pn_capped, phi_j * Mn_j, phi_Pn_j]])

    loop_body = assign("Res", stack(Res, new_row))

    loop_expr = for_loop(
        "j",
        num(2),                         # start
        j <= n_pts,                     # condition
        j + num(1),                     # increment
        loop_body                       # body
    )
    ws.add(MathRegion(
        expr=loop_expr,
        description="Iterar sobre puntos del diagrama"
    ))
    ws.add_spacing(10)

    # Agregar punto de tracción pura al final (M=0, P=P_t)
    P_t = var("P_t")
    row_tension = mat([[num(0) @ "N", P_t,
                        num(0) @ "N", num(0.90) * P_t]])
    ws.add(MathRegion(
        expr=assign("Res", stack(Res, row_tension)),
        description="Agregar punto de tracción pura"
    ))

    # Agregar punto de compresión pura al inicio (M=0, P=P_0.max)
    row_compression = mat([[num(0) @ "N", P0_max_var,
                            num(0) @ "N", num(0.65) * P0_max_var]])
    ws.add(MathRegion(
        expr=assign("Res", stack(row_compression, Res)),
        description="Agregar punto de compresión pura"
    ))

    # ── Extraer vectores columna ──
    ws.add(MathRegion(
        expr=assign("M_nom", col(Res, num(1))),
        description="Vector de momentos nominales"
    ))
    ws.add(MathRegion(
        expr=assign("P_nom", col(Res, num(2))),
        description="Vector de cargas axiales nominales"
    ))
    ws.add(MathRegion(
        expr=assign("M_dis", col(Res, num(3))),
        description="Vector de momentos de diseño (φ·M_n)"
    ))
    ws.add(MathRegion(
        expr=assign("P_dis", col(Res, num(4))),
        description="Vector de cargas axiales de diseño (φ·P_n)"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 12. DIAGRAMA DE INTERACCIÓN — GRÁFICO
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("12. Diagrama de interacción P-M"))

    # Variable de interpolación
    t = var("t")

    # Curva nominal: cinterp parametrizada
    # index = range(1, rows(Res))
    idx = var("idx")
    ws.add(MathRegion(
        expr=assign("idx", range_(num(1), call("rows", Res))),
        description="Índice paramétrico"
    ))

    # Curva nominal: M_n(t) vs P_n(t)
    nom_curve = call("sys",
                     call("linterp", idx, var("M_nom"), t),
                     call("linterp", idx, var("P_nom"), t),
                     num(2), num(1))
    ws.add(MathRegion(
        expr=func_assign("curva_nom", ["t"], nom_curve),
        description="Curva nominal parametrizada"
    ))

    # Curva de diseño: φM_n(t) vs φP_n(t)
    dis_curve = call("sys",
                     call("linterp", idx, var("M_dis"), t),
                     call("linterp", idx, var("P_dis"), t),
                     num(2), num(1))
    ws.add(MathRegion(
        expr=func_assign("curva_dis", ["t"], dis_curve),
        description="Curva de diseño parametrizada (con φ)"
    ))

    # Combinar ambas curvas en un solo plotter
    plotter_expr = call("sys",
                        call("curva_nom", t),
                        call("curva_dis", t),
                        num(2), num(1))
    ws.add(MathRegion(
        expr=func_assign("diagrama", ["t"], plotter_expr),
        description="Diagrama combinado: nominal + diseño"
    ))
    ws.add_spacing(10)

    # Gráfico
    ws.add(PlotRegion(
        inputs=[var("diagrama")],
        plot_type="2d",
        render="lines",
        grid=True,
        axes=True,
        width=500,
        height=400,
    ))

    # ════════════════════════════════════════════════════════════════════
    # 13. VERIFICACIÓN DEL PUNTO DE CARGA
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("13. Verificación del punto de carga"))

    M_u = var("M_u")
    P_u = var("P_u")

    ws.add(MathRegion(
        expr=evaluate("P_u"),
        show_result=True,
        contract_expr=compound_unit(["kN"], []),
        description="Carga axial de diseño"
    ))
    ws.add(MathRegion(
        expr=evaluate("M_u"),
        show_result=True,
        contract_expr=compound_unit(["kN", "m"], []),
        description="Momento de diseño"
    ))
    ws.add_spacing(10)

    # Excentricidad
    e_expr = M_u / P_u
    ws.add(MathRegion(
        expr=assign("e_u", e_expr),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Excentricidad de la carga"
    ))

    # Buscar c tal que M_n(c)/P_n(c) = e_u para obtener Pn y Mn
    # en la dirección del punto de carga
    # Resolvemos: M_n(c_v)/P_n(c_v) = e_u
    e_u = var("e_u")
    c_v = var("c_v")

    cv_expr = call("solve",
                   call("M_n", c_v) / call("P_n", c_v) - e_u,
                   c_v, var("c_b"))
    ws.add(MathRegion(
        expr=assign("c_ver", cv_expr),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Profundidad del eje neutro para la excentricidad de diseño"
    ))
    ws.add_spacing(10)

    c_ver = var("c_ver")

    # φ·Pn y φ·Mn para la excentricidad del punto de carga
    ws.add(MathRegion(
        expr=assign("φP_n.ver", call("φ", c_ver) * call("P_n", c_ver)),
        show_result=True,
        contract_expr=compound_unit(["kN"], []),
        description="φ·P_n en la dirección del punto de carga"
    ))
    ws.add(MathRegion(
        expr=assign("φM_n.ver", call("φ", c_ver) * call("M_n", c_ver)),
        show_result=True,
        contract_expr=compound_unit(["kN", "m"], []),
        description="φ·M_n en la dirección del punto de carga"
    ))
    ws.add_spacing(10)

    # DCR = P_u / (φ·P_n)
    phi_Pn_ver = var("φP_n.ver")
    DCR_expr = P_u / phi_Pn_ver
    ws.add(MathRegion(
        expr=assign("DCR", DCR_expr),
        show_result=True,
        description="Razón demanda/capacidad (debe ser ≤ 1.0)"
    ))

    ws.add(MathRegion(
        expr=evaluate("DCR"),
        show_result=True,
        description="Verificación: DCR ≤ 1.0 → OK"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 14. RESUMEN
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("14. Resumen de resultados"))

    ws.add(MathRegion(
        expr=evaluate("P_0"),
        show_result=True,
        contract_expr=compound_unit(["kN"], []),
        description="Compresión pura nominal"
    ))
    ws.add(MathRegion(
        expr=evaluate("P_0.max"),
        show_result=True,
        contract_expr=compound_unit(["kN"], []),
        description="Capacidad máxima (0.80·P_0)"
    ))
    ws.add(MathRegion(
        expr=evaluate("P_b"),
        show_result=True,
        contract_expr=compound_unit(["kN"], []),
        description="Carga axial balanceada"
    ))
    ws.add(MathRegion(
        expr=evaluate("M_b"),
        show_result=True,
        contract_expr=compound_unit(["kN", "m"], []),
        description="Momento balanceado"
    ))
    ws.add(MathRegion(
        expr=evaluate("M_0"),
        show_result=True,
        contract_expr=compound_unit(["kN", "m"], []),
        description="Momento en flexión pura"
    ))
    ws.add(MathRegion(
        expr=evaluate("P_t"),
        show_result=True,
        contract_expr=compound_unit(["kN"], []),
        description="Tracción pura nominal"
    ))
    ws.add_spacing(10)

    ws.add(MathRegion(
        expr=evaluate("DCR"),
        show_result=True,
        description="DCR final (≤ 1.0 → columna verificada)"
    ))

    # ── Guardar ──
    ws.save("output/Columna_Interaccion.sm")
    print("✓ Guardado output/Columna_Interaccion.sm")


if __name__ == "__main__":
    main()
