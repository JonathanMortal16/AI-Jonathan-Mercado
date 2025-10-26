import random

estados = ["A", "B", "C"]  # C será terminal

# Política fija π(s):
# - En A siempre ve a B
# - En B siempre ve a C
# - En C se termina
politica_fija = {
    "A": "B",
    "B": "C",
    "C": None  # None = no hay acción, estado terminal
}


# Esto simula incertidumbre en el entorno.
def recompensa_final_en_C():
    # escogemos una recompensa aleatoria razonable
    return random.choice([8, 10, 12])


# Estructuras para aprender valores ----------------------
retornos_por_estado = {s: [] for s in estados}
V = {s: 0.0 for s in estados}


# 3. Función para simular UN episodio -----------------------
def ejecutar_un_episodio(estado_inicial="A"):
    """
    Corre la política fija hasta llegar a un estado terminal (C).
    Devuelve:
      - visita: lista de estados visitados en orden
      - R_total: recompensa final obtenida
    """
    estado_actual = estado_inicial
    visita = [estado_actual]

    while True:
        # ¿Ya estamos en estado terminal?
        if politica_fija[estado_actual] is None:
            # estado_actual == "C"
            # Se obtiene recompensa final al terminar el episodio
            R_total = recompensa_final_en_C()
            break

        # Si no es terminal, seguimos la política fija
        siguiente_estado = politica_fija[estado_actual]
        estado_actual = siguiente_estado
        visita.append(estado_actual)

    return visita, R_total


# 4. Entrenamiento pasivo (muchos episodios) ----------------
num_episodios = 20  # puedes subirlo si quieres más estabilidad

for episodio in range(1, num_episodios + 1):
    visita, R_total = ejecutar_un_episodio(estado_inicial="A")

    # Para cada estado que apareció en este episodio,
    # guardamos la recompensa total.
    for estado_visitado in visita:
        retornos_por_estado[estado_visitado].append(R_total)

    # Recalculamos V[s] como el promedio de retornos observados
    for s in estados:
        if len(retornos_por_estado[s]) > 0:
            V[s] = sum(retornos_por_estado[s]) / len(retornos_por_estado[s])

    # Mostramos el progreso
    print(f"--- Episodio {episodio} ---")
    print("Trayectoria seguida:", " -> ".join(visita))
    print("Recompensa total recibida al final:", R_total)
    print("Valores estimados V(s):")
    for s in estados:
        print(f"  V({s}) = {V[s]:.2f}")
    print()


# 5. Resultado final ----------------------------------------
print("====================================")
print("VALORES FINALES ESTIMADOS DESPUES DEL ENTRENAMIENTO:")
for s in estados:
    print(f"V({s}) ≈ {V[s]:.2f}")
print("====================================")