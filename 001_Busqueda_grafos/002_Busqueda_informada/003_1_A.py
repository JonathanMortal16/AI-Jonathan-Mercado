import heapq  # para la cola de prioridad

def reconstruir_camino(came_from, actual):
    """
    Reconstruye el camino desde el inicio hasta 'actual'
    usando el diccionario came_from que guarda padres.
    """
    camino = [actual]
    while actual in came_from:
        actual = came_from[actual]
        camino.append(actual)
    camino.reverse()
    return camino

def a_estrella(grafo, heuristica, inicio, meta):
    """
    Implementación del algoritmo A*.
    
    Parámetros:
    - grafo: dict con las conexiones {nodo: [(vecino, costo_real), ...]}
    - heuristica: dict con h(n) estimado hacia la meta
    - inicio: nodo inicial
    - meta: nodo objetivo

    Regresa:
    - lista con el camino óptimo (menor costo) desde inicio hasta meta
      o None si no se encuentra camino.
    """

    # g_cost[nodo] = mejor costo real conocido desde 'inicio' hasta 'nodo'
    g_cost = {inicio: 0}

    # f_score[nodo] = g_cost[nodo] + h(nodo)
    f_score = {inicio: heuristica[inicio]}

    # came_from[nodo] = padre de 'nodo' en el mejor camino conocido
    came_from = {}

    # frontera: tuplas (f_score, nodo)
    frontera = []
    heapq.heappush(frontera, (f_score[inicio], inicio))

    # Para no reexpandir nodos "cerrados"
    cerrados = set()

    while frontera:
        # Sacar el nodo con menor f_score
        f_actual, actual = heapq.heappop(frontera)

        # Si ya llegamos a la meta, reconstruimos y regresamos el camino óptimo
        if actual == meta:
            return reconstruir_camino(came_from, actual)

        # Si ya estaba cerrado, saltamos
        if actual in cerrados:
            continue
        cerrados.add(actual)

        # Revisar vecinos del nodo actual
        for vecino, costo_real in grafo[actual]:
            # Costo tentativo pasando por 'actual'
            costo_tentativo = g_cost[actual] + costo_real

            # Si este camino al vecino es mejor que cualquier otro conocido
            if vecino not in g_cost or costo_tentativo < g_cost[vecino]:
                came_from[vecino] = actual
                g_cost[vecino] = costo_tentativo
                f_score[vecino] = costo_tentativo + heuristica[vecino]

                # Agregamos el vecino a la frontera con su nueva prioridad
                heapq.heappush(frontera, (f_score[vecino], vecino))

    # Si salimos del while, no hubo ruta
    return None


# ========================
# EJEMPLO DE USO
# ========================
if __name__ == "__main__":
    # Grafo dirigido/no dirigido con costos
    grafo = {
        'A': [('B', 2), ('C', 5)],
        'B': [('A', 2), ('D', 4)],
        'C': [('A', 5), ('D', 1), ('E', 7)],
        'D': [('B', 4), ('C', 1), ('F', 3)],
        'E': [('C', 7), ('G', 3)],
        'F': [('D', 3), ('G', 2)],
        'G': [('E', 3), ('F', 2)]
    }

    # Heurística admisible hacia 'G'
    heuristica = {
        'A': 10,
        'B': 8,
        'C': 5,
        'D': 4,
        'E': 3,
        'F': 2,
        'G': 0
    }

    inicio = 'A'
    meta = 'G'

    camino_optimo = a_estrella(grafo, heuristica, inicio, meta)
    print("Camino óptimo encontrado por A*:")
    print(camino_optimo)
