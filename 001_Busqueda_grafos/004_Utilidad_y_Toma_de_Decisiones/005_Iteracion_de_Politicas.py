# Estados del MDP
estados = ["A", "B", "C"]

# Transiciones con recompensas
# Formato: transiciones[estado][accion] = [(prob, siguiente_estado, recompensa)]
transiciones = {
    "A": {"ir": [(1.0, "B", -0.1)]},
    "B": {"ir": [(1.0, "C", -0.1)]},
    "C": {"terminar": [(1.0, "C", 10.0)]}
}

# Parámetros
gamma = 0.9
theta = 0.001  # Tolerancia para convergencia

# Inicializamos política aleatoria (todas las acciones "ir")
pi = {s: list(transiciones[s].keys())[0] for s in estados}

# Inicializamos valores
V = {s: 0.0 for s in estados}

# ----------------------------------------
# Función para evaluar la política actual
# ----------------------------------------
def evaluar_politica(V, pi):
    while True:
        delta = 0
        for s in estados:
            accion = pi[s]
            suma = 0
            for (prob, s_next, r) in transiciones[s][accion]:
                suma += prob * (r + gamma * V[s_next])
            delta = max(delta, abs(V[s] - suma))
            V[s] = suma
        if delta < theta:
            break

# ----------------------------------------
# Función para mejorar la política
# ----------------------------------------
def mejorar_politica(V, pi):
    policy_stable = True
    for s in estados:
        accion_actual = pi[s]
        acciones = transiciones[s]
        valores_acciones = {}

        for a in acciones:
            suma = 0
            for (prob, s_next, r) in acciones[a]:
                suma += prob * (r + gamma * V[s_next])
            valores_acciones[a] = suma

        # Elegimos la mejor acción
        mejor_accion = max(valores_acciones, key=valores_acciones.get)
        if mejor_accion != accion_actual:
            pi[s] = mejor_accion
            policy_stable = False
    return policy_stable

# ----------------------------------------
# Algoritmo principal de iteración de políticas
# ----------------------------------------
iteracion = 0
while True:
    iteracion += 1
    print(f"\n--- Iteración {iteracion} ---")
    evaluar_politica(V, pi)
    print("Valores:", V)
    estable = mejorar_politica(V, pi)
    print("Política:", pi)
    if estable:
        break

print("\n===== Política Óptima =====")
for s in estados:
    print(f"Estado {s} -> Acción óptima: {pi[s]}")
print("=============================")
