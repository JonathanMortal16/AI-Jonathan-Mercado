import random
# --- 1. Definición del entorno ---------------------------------

estados = ["A", "B", "C", "META"]

acciones_posibles = {
    "A": ["izq", "der"],
    "B": ["izq", "der"],
    "C": ["izq", "der"],
    "META": []
}

def transicion(estado, accion):
    """Simula la transición de estado y devuelve (nuevo_estado, recompensa, terminado)."""
    if estado == "META":
        return "META", 0, True

    if accion == "der":
        if estado == "A": return "B", 0, False
        if estado == "B": return "C", 0, False
        if estado == "C": return "META", 10, True

    if accion == "izq":
        if estado == "C": return "B", 0, False
        if estado == "B": return "A", 0, False
        if estado == "A": return "A", 0, False  # se queda en A

    return estado, 0, False


# --- 2. Inicialización de parámetros ----------------------------

Q = {s: {a: 0.0 for a in acciones_posibles[s]} for s in estados}

alpha = 0.5     # tasa de aprendizaje
gamma = 0.9     # factor de descuento
epsilon = 0.2   # probabilidad de explorar
episodios = 40   # cantidad de episodios


# --- 3. Función para elegir acción (epsilon-greedy) -------------
def elegir_accion(estado):
    acciones = acciones_posibles[estado]
    if len(acciones) == 0:
        return None

    # Con probabilidad epsilon, elige una acción aleatoria (explora)
    if random.random() < epsilon:
        return random.choice(acciones)

    # Si no, elige la mejor según Q
    return max(acciones, key=lambda a: Q[estado][a])


# --- 4. Ciclo de aprendizaje Q-Learning -------------------------
for ep in range(1, episodios + 1):
    estado = "A"
    terminado = False

    while not terminado:
        accion = elegir_accion(estado)
        if accion is None:
            break

        nuevo_estado, recompensa, terminado = transicion(estado, accion)

        # Regla de actualización de Q-Learning
        max_q_siguiente = 0 if terminado else max(Q[nuevo_estado].values())
        Q[estado][accion] = Q[estado][accion] + alpha * (
            recompensa + gamma * max_q_siguiente - Q[estado][accion]
        )

        estado = nuevo_estado

    # Mostrar resultados por episodio
    print(f"--- Episodio {ep} terminado ---")
    for s in ["A", "B", "C"]:
        print(f"Q({s}, der) = {Q[s]['der']:.2f}   Q({s}, izq) = {Q[s]['izq']:.2f}")
    print()


# --- 5. Política final aprendida --------------------------------
print("====================================")
print("POLÍTICA FINAL APRENDIDA:")
for s in ["A", "B", "C"]:
    mejor_accion = max(Q[s], key=lambda a: Q[s][a])
    print(f"En estado {s} -> tomar acción '{mejor_accion}'")
print("====================================")