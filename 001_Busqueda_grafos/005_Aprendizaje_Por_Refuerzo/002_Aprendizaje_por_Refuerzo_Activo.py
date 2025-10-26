import random
# Estados en línea hasta llegar a META
estados = ["A", "B", "C", "META"]

# Acciones posibles (en META no hay acciones)
acciones_posibles = {
    "A": ["izq", "der"],
    "B": ["izq", "der"],
    "C": ["izq", "der"],
    "META": []
}

# Función de transición: dado (estado, acción) -> (nuevo_estado, recompensa_inmediata, terminado)
def transicion(estado, accion):
    # Si ya estamos en META, ya se acabó
    if estado == "META":
        return "META", 0, True  # no te mueves

    # Movimiento hacia la derecha
    if accion == "der":
        if estado == "A":
            return "B", 0, False
        elif estado == "B":
            return "C", 0, False
        elif estado == "C":
            # Llegamos a META: recompensa grande
            return "META", 10, True

    # Movimiento hacia la izquierda
    if accion == "izq":
        if estado == "C":
            return "B", 0, False
        elif estado == "B":
            return "A", 0, False
        elif estado == "A":
            # Izquierda en A = te quedas atorado en A (pierdes el tiempo)
            return "A", 0, False

    # default de seguridad
    return estado, 0, False


#Estructuras de aprendizaje -----------------------------

# Q[s][a] = valor estimado de tomar acción a en estado s
Q = {s: {a: 0.0 for a in acciones_posibles[s]} for s in estados}

# Para calcular promedios, guardamos todas las recompensas vistas
# después de tomar (s,a) en un episodio completo.
retornos_sa = { (s,a): [] for s in ["A","B","C"] for a in acciones_posibles[s] }

# Parámetro de exploración (epsilon)
epsilon = 0.2  # 20% de las veces probamos algo aleatorio


def elegir_accion_epsilon_greedy(estado):
    acciones = acciones_posibles[estado]
    if len(acciones) == 0:
        return None  # en META no hay acción

    # Explorar
    if random.random() < epsilon:
        return random.choice(acciones)

    # Explotar: elegimos la acción con Q más alto
    mejor_accion = None
    mejor_valor = None
    for a in acciones:
        valor_a = Q[estado][a]
        if (mejor_valor is None) or (valor_a > mejor_valor):
            mejor_valor = valor_a
            mejor_accion = a
    return mejor_accion


# 3. Función para ejecutar UN episodio completo -------------
def ejecutar_episodio():
    """
    Corre el agente desde A hasta que llegue a META.
    Devuelve:
      trayectoria: lista de (estado, accion) tomados antes de terminar
      R_total: suma de recompensas obtenidas en el episodio
    """
    estado = "A"
    terminado = False
    trayectoria = []  # [(estado_t, accion_t), ...]
    R_total = 0

    while not terminado:
        accion = elegir_accion_epsilon_greedy(estado)
        if accion is None:
            # estamos en META
            break

        nuevo_estado, recompensa, terminado = transicion(estado, accion)

        trayectoria.append((estado, accion))
        R_total += recompensa

        estado = nuevo_state = nuevo_estado

    return trayectoria, R_total


# 4. Entrenamiento activo (muchos episodios) ----------------
num_episodios = 30

for episodio in range(1, num_episodios + 1):
    trayectoria, R_total = ejecutar_episodio()

    # Guardamos el retorno total para cada (s,a) que usamos
    vistos_este_ep = set()  # para no duplicar si repetimos el mismo par (s,a) en un episodio
    for (s, a) in trayectoria:
        if (s, a) not in vistos_este_ep:
            retornos_sa[(s,a)].append(R_total)
            # actualizamos Q[s][a] = promedio de retornos_sa[(s,a)]
            Q[s][a] = sum(retornos_sa[(s,a)]) / len(retornos_sa[(s,a)])
            vistos_este_ep.add((s,a))

    # Mostramos progreso del episodio
    print(f"--- Episodio {episodio} ---")
    print("Trayectoria (estado,accion):", trayectoria)
    print("Recompensa total recibida:", R_total)
    print("Q actual:")
    for s in ["A","B","C"]:
        for a in acciones_posibles[s]:
            print(f"  Q({s},{a}) = {Q[s][a]:.2f}")
    print()

# 5. Política final aprendida -------------------------------
print("====================================")
print("POLÍTICA APRENDIDA (mejor acción por estado):")
for s in ["A","B","C"]:
    # elegimos la acción con valor Q más alto
    mejor_accion = max(Q[s], key=lambda a: Q[s][a])
    print(f"En estado {s} -> tomar acción '{mejor_accion}'")
print("====================================")

