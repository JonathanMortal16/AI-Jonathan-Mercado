import heapq  # heapq nos da una cola de prioridad mínima

def greedy_best_first_search(grafo, heuristica, inicio, meta):
    # 'frontera' = nodos que queremos visitar, ordenados por h(n)
    # guardaremos tuplas (h(nodo), nodo, camino_hasta_ahora)
    frontera = []
    heapq.heappush(frontera, (heuristica[inicio], inicio, [inicio]))

    visitados = set()  # para no repetir nodos

    while frontera:
        # Sacamos el nodo con menor heurística estimada
        h_actual, nodo_actual, camino = heapq.heappop(frontera)

        # ¿Ya llegamos?
        if nodo_actual == meta:
            return camino  # devolvemos el camino encontrado

        # Marcamos como visitado
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        # Revisamos vecinos del nodo actual
        for vecino, costo in grafo[nodo_actual]:
            if vecino not in visitados:
                nuevo_camino = camino + [vecino]
                heapq.heappush(
                    frontera,
                    (heuristica[vecino], vecino, nuevo_camino)
                )

    # Si no hay camino posible
    return None


# ==========================
# EJEMPLO DE USO
# ==========================

# Definimos el grafo como lista de adyacencia:
# Cada entrada es: nodo : [(vecino, costo_real), ...]
grafo = {
    'A': [('B', 2), ('C', 5)],
    'B': [('A', 2), ('D', 4)],
    'C': [('A', 5), ('D', 1), ('E', 7)],
    'D': [('B', 4), ('C', 1), ('F', 3)],
    'E': [('C', 7), ('G', 3)],
    'F': [('D', 3), ('G', 2)],
    'G': [('E', 3), ('F', 2)]
}

# Heurística h(n): "qué tan cerca creo que está de G"
heuristica = {
    'A': 10,
    'B': 8,
    'C': 5,
    'D': 4,
    'E': 3,
    'F': 2,
    'G': 0
}

camino = greedy_best_first_search(grafo, heuristica, 'A', 'G')
print("Camino encontrado (Greedy Best-First):", camino)
