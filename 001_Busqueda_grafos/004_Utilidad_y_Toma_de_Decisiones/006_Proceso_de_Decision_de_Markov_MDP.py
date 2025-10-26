# 1) Definimos los componentes del MDP
estados = ["A", "B", "C"]

acciones = {
    "A": ["avanzar"],
    "B": ["avanzar"],
    "C": ["terminar"]
}

# Transiciones: P(s' | s, a) y recompensas R(s, a, s')
transiciones = {
    "A": {"avanzar": [(1.0, "B", -0.1)]},
    "B": {"avanzar": [(1.0, "C", -0.1)]},
    "C": {"terminar": [(1.0, "C", 10.0)]}
}

gamma = 0.9  # factor de descuento

# 2) Inicializamos los valores de los estados
V = {s: 0.0 for s in estados}

# 3) Iteración de valores (para resolver el MDP)
for iteracion in range(10):
    print(f"\nIteración {iteracion+1}")
    nuevos_V = V.copy()
    for s in estados:
        valores_acciones = []
        for a in acciones[s]:
            suma = 0
            for (prob, s_next, recompensa) in transiciones[s][a]:
                suma += prob * (recompensa + gamma * V[s_next])
            valores_acciones.append(suma)
        nuevos_V[s] = max(valores_acciones)
        print(f"V({s}) = {nuevos_V[s]:.3f}")
    V = nuevos_V

print("\n===== Valores Finales (V*) =====")
for s in estados:
    print(f"V*({s}) = {V[s]:.3f}")
