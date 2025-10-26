# 1. Probabilidades del nodo de azar (Clima)
prob_lluvia = 0.3
prob_no_lluvia = 0.7

# 2. Tabla de utilidades U(Decisión, Clima)
utilidad = {
    ("llevar", "lluvia"): 100,      # seco
    ("llevar", "no_lluvia"): -20,   # carga peso innecesario
    ("no_llevar", "lluvia"): -100,  # se moja
    ("no_llevar", "no_lluvia"): 50  # ligero y cómodo
}

# 3. Calculamos la utilidad esperada de cada decisión
def utilidad_esperada(decision):
    """
    Calcula la utilidad esperada según el clima.
    EU(D) = sum(P(clima) * U(decision, clima))
    """
    eu = 0
    eu += prob_lluvia * utilidad[(decision, "lluvia")]
    eu += prob_no_lluvia * utilidad[(decision, "no_lluvia")]
    return eu

# 4. Decisiones posibles
decisiones = ["llevar", "no_llevar"]

# 5. Evaluamos todas las decisiones
for d in decisiones:
    print(f"Decisión: {d}")
    print(f"  Utilidad esperada = {utilidad_esperada(d)}")
    print()

# 6. Elegimos la mejor decisión
mejor_decision = max(decisiones, key=utilidad_esperada)
print("========================================")
print(f"La mejor decisión es: '{mejor_decision}'")
print(f"Con utilidad esperada = {utilidad_esperada(mejor_decision)}")
print("========================================")
