# Definimos los estados
estados = ["A", "B", "C"]

# Definimos las transiciones y recompensas
# Formato: transiciones[estado][accion] = [(probabilidad, siguiente_estado, recompensa)]
transiciones = {
    "A": {"ir": [(1.0, "B", -0.1)]},
    "B": {"ir": [(1.0, "C", -0.1)]},
    "C": {"terminar": [(1.0, "C", 1.0)]}  # Estado terminal, da +1
}

# Parámetros del MDP
gamma = 0.9   # Factor de descuento
theta = 0.001 # Tolerancia de convergencia

# Inicializamos los valores de los estados
V = {s: 0.0 for s in estados}

# Algoritmo de iteración de valores
while True:
    delta = 0
    for s in estados:
        acciones = transiciones[s]
        nuevos_valores = []

        for a in acciones:
            suma = 0
            for (prob, s_next, recompensa) in acciones[a]:
                suma += prob * (recompensa + gamma * V[s_next])
            nuevos_valores.append(suma)

        # Tomamos la mejor acción posible
        nuevo_valor = max(nuevos_valores)
        delta = max(delta, abs(V[s] - nuevo_valor))
        V[s] = nuevo_valor

    # Si los valores ya no cambian mucho, paramos
    if delta < theta:
        break

# Mostramos los valores finales
print("===== Valores Óptimos de los Estados =====")
for s in estados:
    print(f"V({s}) = {V[s]:.3f}")
