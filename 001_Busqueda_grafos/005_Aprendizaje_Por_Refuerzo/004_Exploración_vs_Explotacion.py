import random
# --- 1. Definimos el entorno ---------------------------------
estados = ["A", "B", "C", "META"]
acciones_posibles = {
    "A": ["izq", "der"],
    "B": ["izq", "der"],
    "C": ["izq", "der"],
    "META": []
}

def transicion(estado, accion):
    """Simula el cambio de estado."""
    if estado == "META":
        return "META", 0, True
    if accion == "der":
        if estado == "A": return "B", 0, False
        if estado == "B": return "C", 0, False
        if estado == "C": return "META", 10, True
    if accion == "izq":
        if estado == "C": return "B", 0, False
        if estado == "B": return "A", 0, False
        if estado == "A": return "A", 0, False
    return estado, 0, False


# --- 2. Parámetros de Q-Learning ------------------------------
def entrenar_qlearning(epsilon, episodios=30):
    """Entrena un agente Q-learning con un epsilon dado."""
    alpha = 0.5
    gamma = 0.9
    Q = {s: {a: 0.0 for a in acciones_posibles[s]} for s in estados}

    for ep in range(episodios):
        estado = "A"
        terminado = False
        while not terminado:
            # Política epsilon-greedy
            acciones = acciones_posibles[estado]
            if len(acciones) == 0:
                break
            if random.random() < epsilon:
                accion = random.choice(acciones)  # explorar
            else:
                accion = max(acciones, key=lambda a: Q[estado][a])  # explotar

            nuevo_estado, recompensa, terminado = transicion(estado, accion)
            max_q_siguiente = 0 if terminado else max(Q[nuevo_estado].values())

            # Actualización Q-Learning
            Q[estado][accion] += alpha * (
                recompensa + gamma * max_q_siguiente - Q[estado][accion]
            )

            estado = nuevo_estado
    return Q


# --- 3. Comparación de exploración alta vs baja ---------------
Q_explora = entrenar_qlearning(epsilon=0.9)
Q_explota = entrenar_qlearning(epsilon=0.1)

# --- 4. Mostrar resultados ------------------------------------
print("====================================")
print("AGENTE CON MUCHA EXPLORACIÓN (ε = 0.9):")
for s in ["A", "B", "C"]:
    mejor = max(Q_explora[s], key=lambda a: Q_explora[s][a])
    print(f"  En estado {s} -> acción preferida: {mejor}")

print("\nAGENTE CON POCA EXPLORACIÓN (ε = 0.1):")
for s in ["A", "B", "C"]:
    mejor = max(Q_explota[s], key=lambda a: Q_explota[s][a])
    print(f"  En estado {s} -> acción preferida: {mejor}")
print("====================================")
