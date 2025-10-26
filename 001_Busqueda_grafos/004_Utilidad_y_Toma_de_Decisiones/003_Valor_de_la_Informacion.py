# Probabilidades del clima
prob_lluvia = 0.3
prob_no_lluvia = 0.7

# Utilidades
utilidad = {
    ("llevar", "lluvia"): 100,
    ("llevar", "no_lluvia"): -20,
    ("no_llevar", "lluvia"): -100,
    ("no_llevar", "no_lluvia"): 50
}

# Función para utilidad esperada de una decisión fija
def utilidad_esperada(decision):
    return (
        prob_lluvia * utilidad[(decision, "lluvia")] +
        prob_no_lluvia * utilidad[(decision, "no_lluvia")]
    )

# 1) Sin información (decisión fija)
eu_llevar = utilidad_esperada("llevar")
eu_no_llevar = utilidad_esperada("no_llevar")
eu_sin_info = max(eu_llevar, eu_no_llevar)
mejor_sin_info = "llevar" if eu_llevar > eu_no_llevar else "no_llevar"

print("===== SIN INFORMACIÓN =====")
print(f"Decisión elegida: {mejor_sin_info}")
print(f"Utilidad esperada sin información: {eu_sin_info}\n")

# 2) Con información perfecta (decisión óptima según cada caso)
eu_con_info = (
    prob_lluvia * max(utilidad[("llevar", "lluvia")],
                      utilidad[("no_llevar", "lluvia")]) +
    prob_no_lluvia * max(utilidad[("llevar", "no_lluvia")],
                         utilidad[("no_llevar", "no_lluvia")])
)

print("===== CON INFORMACIÓN PERFECTA =====")
print(f"Utilidad esperada con información: {eu_con_info}\n")

# 3) Valor de la información
voi = eu_con_info - eu_sin_info
print("===== RESULTADO FINAL =====")
print(f"Valor de la Información (VOI) = {voi}")
print("===============================")
