"""Diseño y verificación de viga de hormigón armado según ACI 318-19."""

from smathpy import Worksheet, TextRegion, MathRegion, var, assign, evaluate, num
from smathpy.expression import sum_, func_assign, call, mat
from smathpy.expression.functions import sqrt
from smathpy.units import with_unit, value_with_compound_unit, compound_unit
# ── Control structures ─────────────────────────────────────────────────────
from smathpy.expression import (
    line, range_, for_range, for_loop, while_loop, if_, sum_, product_,
)

def main():
    ws = Worksheet(title="Viga de Hormigón Armado ACI318-19", author="FCB")

    # ════════════════════════════════════════════════════════════════════
    # TÍTULO
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.title("Diseño y Verificación de Viga de Hormigón Armado — ACI 318-19"))

    # ════════════════════════════════════════════════════════════════════
    # 1. DATOS DE ENTRADA — GEOMETRÍA
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("1. Geometría de la sección"))

    ws.add(MathRegion.assignment("b", 300, unit_name="mm",
                                  description="Ancho de la viga"))
    ws.add(MathRegion.assignment("h", 500, unit_name="mm",
                                  description="Altura total de la viga"))
    ws.add(MathRegion.assignment("r", 40, unit_name="mm",
                                  description="Recubrimiento libre"))

    # ════════════════════════════════════════════════════════════════════
    # 2. DATOS DE ENTRADA — MATERIALES
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("2. Propiedades de los materiales"))

    ws.add(MathRegion.assignment("f'_c", 25, unit_name="MPa",
                                  description="Resistencia a compresión del hormigón"))
    ws.add(MathRegion.assignment("f_y", 420, unit_name="MPa",
                                  description="Fluencia del acero longitudinal"))
    ws.add(MathRegion.assignment("f_yt", 420, unit_name="MPa",
                                  description="Fluencia del acero transversal"))
    ws.add(MathRegion.assignment("E_s", 200000, unit_name="MPa",
                                  description="Módulo de elasticidad del acero"))

    # ════════════════════════════════════════════════════════════════════
    # 3. DATOS DE ENTRADA — ARMADURA LONGITUDINAL
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("3. Armadura longitudinal propuesta"))

    ws.add(MathRegion.assignment("n_b", 3,
                                  description="Número de barras en tracción"))
    ws.add(MathRegion.assignment("d_b", 22, unit_name="mm",
                                  description="Diámetro de barras longitudinales"))
    ws.add(MathRegion.assignment("d_e", 10, unit_name="mm",
                                  description="Diámetro del estribo"))

    # ════════════════════════════════════════════════════════════════════
    # 4. DATOS DE ENTRADA — SOLICITACIONES
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("4. Solicitaciones de diseño"))

    ws.add(MathRegion(
        expr=assign("M_u", value_with_compound_unit(120, ["kN", "m"], []) ),
        description="Momento último de diseño"
    ))
    ws.add(MathRegion(
        expr=assign("V_u", num(80) @ "kN"),
        description="Corte último de diseño"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 5. PROPIEDADES CALCULADAS
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("5. Propiedades calculadas"))

    # Altura efectiva: d = h - r - d_e - d_b/2
    b = var("b")
    h = var("h")
    r = var("r")
    d_b = var("d_b")
    d_e = var("d_e")
    n_b = var("n_b")
    f_c = var("f'_c")
    f_y = var("f_y")
    f_yt = var("f_yt")
    E_s = var("E_s")

    d_expr = h - r - d_e - d_b / num(2)
    ws.add(MathRegion(
        expr=assign("d", d_expr),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Altura efectiva"
    ))

    # Área de una barra: A_b = π/4 * d_b²
    pi = var("π")
    A_b_expr = pi / num(4) * d_b ** num(2)
    ws.add(MathRegion(
        expr=assign("A_b", A_b_expr),
        show_result=True,
        contract_expr=compound_unit(["mm","mm"], []),
        description="Área de una barra"
    ))
    ws.add_spacing(10)

    # Área de acero total: A_s = n_b * A_b
    A_b = var("A_b")
    A_s_expr = n_b * A_b
    ws.add(MathRegion(
        expr=assign("A_s", A_s_expr),
        show_result=True,
        contract_expr=compound_unit(["mm","mm"], []),
        description="Área de acero en tracción"
    ))


    # ════════════════════════════════════════════════════════════════════
    # 6. MÓDULO DE ROTURA Y RESISTENCIA DEL HORMIGÓN (ACI 318-19 §19.2)
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("6. Propiedades del hormigón — ACI 318-19 §19.2"))

    # λ = 1.0 (hormigón de peso normal)
    ws.add(MathRegion.assignment("λ", 1,
                                  description="Factor de hormigón liviano (peso normal)"))

    # fr = 0.62·λ·√(f'c)  — Módulo de rotura (§19.2.3.1)
    lam = var("λ")
    fr_expr = num(0.62) * lam * sqrt(f_c * (num(1) @ "MPa"))
    ws.add(MathRegion(
        expr=assign("f_r", fr_expr),
        show_result=True,
        contract_expr=compound_unit(["MPa"], []),
        description="Módulo de rotura — ACI 19.2.3.1"
    ))

    # β1 según f'c (§22.2.2.4.3)
    # β1 = 0.85 para f'c ≤ 28 MPa (simplificado)
    ws.add(MathRegion.assignment("β_1", 0.85,
                                  description="Factor del bloque de compresión — ACI 22.2.2.4.3"))

    # ════════════════════════════════════════════════════════════════════
    # 7. DISEÑO A FLEXIÓN (ACI 318-19 §22.2)
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("7. Diseño a flexión — ACI 318-19 §22.2"))

    A_s = var("A_s")
    d = var("d")
    beta1 = var("β_1")

    # Profundidad del bloque de compresión: a = As·fy / (0.85·f'c·b)
    a_expr = A_s * f_y / (num(0.85) * f_c * b)
    ws.add(MathRegion(
        expr=assign("a", a_expr),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Profundidad del bloque de compresión"
    ))
    ws.add_spacing(10)

    a = var("a")

    # Profundidad del eje neutro: c = a / β1
    c_expr = a / beta1
    ws.add(MathRegion(
        expr=assign("c", c_expr),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Profundidad del eje neutro"
    ))
    ws.add_spacing(10)

    c = var("c")

    # Deformación en el acero: εt = 0.003·(d - c) / c  (§22.2.2.1)
    eps_t_expr = num(0.003) * (d - c) / c
    ws.add(MathRegion(
        expr=assign("ε_t", eps_t_expr),
        show_result=True,
        description="Deformación unitaria en el acero en tracción"
    ))

    eps_t = var("ε_t")

    # Verificación de ductilidad: εt ≥ 0.005 para sección controlada por tracción
    # εy = fy / Es
    eps_y_expr = f_y / E_s
    ws.add(MathRegion(
        expr=assign("ε_y", eps_y_expr),
        show_result=True,
        description="Deformación de fluencia del acero"
    ))
    ws.add_spacing(10)
    # ════════════════════════════════════════════════════════════════════
    # 8. FACTOR DE REDUCCIÓN φ (ACI 318-19 §21.2)
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("8. Factor de reducción φ — ACI 318-19 §21.2"))

    # Para secciones controladas por tracción (εt ≥ 0.005): φ = 0.90
    # Para transición (0.002 ≤ εt < 0.005): φ interpolado
    # Simplificado: asumimos controlada por tracción
    ws.add(MathRegion.assignment("φ_f", 0.9,
                                  description="Factor φ para flexión (controlada por tracción)"))

    phi_f = var("φ_f")

    # ════════════════════════════════════════════════════════════════════
    # 9. MOMENTO NOMINAL Y VERIFICACIÓN (ACI 318-19 §22.3)
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("9. Momento resistente — ACI 318-19 §22.3"))

    # Mn = As·fy·(d - a/2)
    M_n_expr = A_s * f_y * (d - a / num(2))
    ws.add(MathRegion(
        expr=assign("M_n", M_n_expr),
        show_result=True,
        contract_expr=compound_unit(["tonnef","m"], []),
        description="Momento nominal"
    ))
    ws.add_spacing(10)

    M_n = var("M_n")

    # φMn
    phi_Mn_expr = phi_f * M_n
    ws.add(MathRegion(
        expr=assign("φM_n", phi_Mn_expr),
        show_result=True,
        contract_expr=compound_unit(["tonnef","m"], []),
        description="Momento resistente de diseño"
    ))

    # Evaluación φMn
    ws.add(MathRegion(
        expr=evaluate("φM_n"),
        show_result=True,
        contract_expr=compound_unit(["tonnef","m"], []),
        description="Valor de φMn"
    ))

    # Ratio Mu / φMn
    M_u = var("M_u")
    phi_Mn = var("φM_n")
    ratio_f_expr = M_u / phi_Mn
    ws.add(MathRegion(
        expr=assign("DCR_f", ratio_f_expr),
        show_result=True,
        description="Razón demanda/capacidad a flexión"
    ))
    ws.add_spacing(10)

    ws.add(MathRegion(
        expr=evaluate("DCR_f"),
        show_result=True,
        description="Verificación: DCR_f ≤ 1.0 → OK"
    ))
    ws.add_spacing(10)

    # ════════════════════════════════════════════════════════════════════
    # 10. CUANTÍAS MÍNIMA Y MÁXIMA (ACI 318-19 §9.6.1)
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("10. Cuantías límite — ACI 318-19 §9.6.1"))

    # ρ_min = max([0.25·√(f'c·1MPa)/fy, 1.4MPa/fy])  — §9.6.1.2
    rho_min_1 = num(0.25) * sqrt(f_c * (num(1) @ "MPa")) / f_y
    rho_min_2 = (num(1.4) @ "MPa") / f_y
    rho_min_expr = call("max", mat([[rho_min_1], [rho_min_2]]))  # vector columna [rho1; rho2]
    ws.add(MathRegion(
        expr=assign("ρ_min", rho_min_expr),
        show_result=True,
        description="Cuantía mínima — ACI 9.6.1.2"
    ))
    ws.add_spacing(50)

    # As_min = ρ_min · b · d
    rho_min = var("ρ_min")
    As_min_expr = rho_min * b * d
    ws.add(MathRegion(
        expr=assign("A_s.min", As_min_expr),
        show_result=True,
        contract_expr=compound_unit(["mm", "mm"], []),
        description="Área de acero mínima"
    ))

    # ρ = As / (b·d)
    rho_expr = A_s / (b * d)
    ws.add(MathRegion(
        expr=assign("ρ", rho_expr),
        show_result=True,
        description="Cuantía de acero provista"
    ))
    ws.add_spacing(10)

    ws.add(MathRegion(
        expr=evaluate("ρ"),
        description="Valor de cuantía provista"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 11. DISEÑO A CORTE (ACI 318-19 §22.5)
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("11. Diseño a corte — ACI 318-19 §22.5"))

    ws.add(MathRegion.assignment("φ_v", 0.75,
                                  description="Factor φ para corte"))

    phi_v = var("φ_v")

    # Vc = 0.17·λ·√(f'c)·b·d  (§22.5.5.1 — simplificado)
    V_c_expr = num(0.17) * lam * sqrt(f_c * (num(1) @ "MPa")) * b * d
    ws.add(MathRegion(
        expr=assign("V_c", V_c_expr),
        show_result=True,
        contract_expr=compound_unit(["tonnef"], []),
        description="Resistencia al corte del hormigón — ACI 22.5.5.1"
    ))

    V_c = var("V_c")

    # φVc
    phi_Vc_expr = phi_v * V_c
    ws.add(MathRegion(
        expr=assign("φV_c", phi_Vc_expr),
        show_result=True,
        contract_expr=compound_unit(["tonnef"], []),
        description="Resistencia de diseño al corte del hormigón"
    ))

    ws.add(MathRegion(
        expr=evaluate("φV_c"),
        show_result=True,
        contract_expr=compound_unit(["tonnef"], []),
        description="Valor de φVc"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 12. ARMADURA TRANSVERSAL (ACI 318-19 §22.5.10)
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("12. Armadura transversal — ACI 318-19 §22.5.10"))

    V_u = var("V_u")
    phi_Vc = var("φV_c")

    # Vs requerido: Vs = (Vu/φv) - Vc
    V_s_req_expr = V_u / phi_v - V_c
    ws.add(MathRegion(
        expr=assign("V_s", V_s_req_expr),
        show_result=True,
        contract_expr=compound_unit(["tonnef"], []),
        description="Resistencia al corte requerida del acero"
    ))
    ws.add_spacing(10)

    ws.add(MathRegion(
        expr=evaluate("V_s"),
        show_result=True,
        contract_expr=compound_unit(["tonnef"], []),
        description="Valor de Vs"
    ))

    V_s = var("V_s")

    # Área del estribo (2 ramas): Av = 2 · π/4 · de²
    A_v_expr = num(2) * pi / num(4) * d_e ** num(2)
    ws.add(MathRegion(
        expr=assign("A_v", A_v_expr),
        show_result=True,
        contract_expr=compound_unit(["mm","mm"], []),
        description="Área del estribo (2 ramas)"
    ))
    ws.add_spacing(10)

    A_v = var("A_v")

    # Separación requerida: s = Av·fyt·d / Vs  (§22.5.10.5.3)
    s_req_expr = A_v * f_yt * d / V_s
    ws.add(MathRegion(
        expr=assign("s_req", s_req_expr),
        description="Separación requerida de estribos"
    ))
    ws.add_spacing(10)

    ws.add(MathRegion(
        expr=evaluate("s_req"),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Valor de separación requerida"
    ))

    # ════════════════════════════════════════════════════════════════════
    # 13. SEPARACIÓN MÁXIMA DE ESTRIBOS (ACI 318-19 §9.7.6.2.2)
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("13. Separación máxima — ACI 318-19 §9.7.6.2.2"))

    # s_max = min([d/2, 600mm]) para Vs ≤ 0.33·√(f'c)·b·d
    s_max_expr = call("min", mat([[d / num(2)], [num(600) @ "mm"]]))  # vector columna [d/2; 600mm]
    ws.add(MathRegion(
        expr=assign("s_max", s_max_expr),
        show_result=True,
        contract_unit="mm",
        description="Separación máxima de estribos"
    ))
    ws.add_spacing(40)

    # ════════════════════════════════════════════════════════════════════
    # 14. RESUMEN DE VERIFICACIONES
    # ════════════════════════════════════════════════════════════════════
    ws.add(TextRegion.section("14. Resumen de verificaciones"))

    ws.add(MathRegion(
        expr=evaluate("DCR_f"),
        show_result=True,
        description="DCR flexión (debe ser ≤ 1.0)"
    ))

    ws.add(MathRegion(
        expr=evaluate("ε_t"),
        show_result=True,
        description="Deformación del acero (debe ser ≥ 0.005 para control por tracción)"
    ))

    ws.add(MathRegion(
        expr=evaluate("ρ"),
        show_result=True,
        description="Cuantía provista (debe ser ≥ ρ_min)"
    ))

    ws.add(MathRegion(
        expr=evaluate("ρ_min"),
        show_result=True,
        description="Cuantía mínima"
    ))

    ws.add(MathRegion(
        expr=evaluate("s_req"),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Separación requerida de estribos"
    ))

    ws.add(MathRegion(
        expr=evaluate("s_max"),
        show_result=True,
        contract_expr=compound_unit(["mm"], []),
        description="Separación máxima de estribos"
    ))

    # ── Guardar ──
    ws.save("output/Viga_HA_ACI318.sm")
    print("✓ Guardado output/Viga_HA_ACI318.sm")


if __name__ == "__main__":
    main()