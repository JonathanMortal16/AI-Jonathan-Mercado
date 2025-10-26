import heapq  # heapq nos da una cola de prioridad mínima (min-heap)

def greedy_best_first_search(grafo, heuristica, inicio, meta):
    """
    Implementa Búsqueda Voraz Primero el Mejor (Greedy Best-First Search).
    Selecciona siempre el siguiente nodo con la heurística h(n) más baja.

    Parámetros:
    - grafo: diccionario con las conexiones {nodo: [(vecino, costo), ...]}
    - heuristica: diccionario con valores h(n) estimados hacia la meta
    - inicio: nodo inicial
    - meta: nodo objetivo

    Regresa:
    - lista con el camino desde 'inicio' hasta 'meta', o None si no hay camino
    """

    # 'frontera' es la lista de candidatos a explorar.
    # Cada elemento será una tupla: (h(nodo), nodo, camino_hasta_nodo)
    frontera = []
    heapq.heappush(frontera, (heuristica[inicio], inicio, [inicio]))

    # Conjunto de visitados para no re-explorar nodos y evitar ciclos.
    visitados = set()

    while frontera:
        # Sacamos el nodo "más prometedor" según h(n)
        h_actual, nodo_actual, camino_actual = heapq.heappop(frontera)

        # Si ya llegamos a la meta, regresamos el camino
        if nodo_actual == meta:
            return camino_actual

        # Si ya lo habíamos procesado, lo saltamos
        if nodo_actual in visitados:
            continue

        # Marcamos este nodo como visitado
        visitados.add(nodo_actual)

        # Exploramos cada vecino del nodo actual
        for vecino, costo_real in grafo[nodo_actual]:
            if vecino not in visitados:
                # Construimos el nuevo camino agregando el vecino
                nuevo_camino = camino_actual + [vecino]

                # Insertamos en la frontera ordenado por la heurística h(vecino)
                heapq.heappush(
                    frontera,
                    (heuristica[vecino], vecino, nuevo_camino)
                )

    # Si la frontera se vacía y nunca llegamos a la meta, no hay solución
    return None


# ========================
# EJEMPLO DE USO
# ========================
if __name__ == "__main__":
    # Definimos el grafo como lista de adyacencia.
    # Cada nodo tiene una lista de (vecino, costo_real_de_esa_arista)
    grafo = {
        'A': [('B', 2), ('C', 5)],
        'B': [('A', 2), ('D', 4)],
        'C': [('A', 5), ('D', 1), ('E', 7)],
        'D': [('B', 4), ('C', 1), ('F', 3)],
        'E': [('C', 7), ('G', 3)],
        'F': [('D', 3), ('G', 2)],
        'G': [('E', 3), ('F', 2)]
    }

    # Heurística h(n): estimación de qué tan cerca estoy de 'G'
    heuristica = {
        'A': 10,
        'B': 8,
        'C': 5,
        'D': 4,
        'E': 3,
        'F': 2,
        'G': 0  # la meta siempre tiene heurística 0
    }

    inicio = 'A'
    meta = 'G'

    camino = greedy_best_first_search(grafo, heuristica, inicio, meta)

    print("Camino encontrado por Búsqueda Voraz Primero el Mejor:")
    print(camino)
