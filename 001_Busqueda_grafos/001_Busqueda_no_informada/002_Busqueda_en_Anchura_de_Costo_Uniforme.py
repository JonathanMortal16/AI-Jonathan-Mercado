import heapq  # Cola de prioridad (min-heap)

def busqueda_costo_uniforme(grafo, inicio, meta):
    """
    Implementación simple de Búsqueda en Anchura de Costo Uniforme (UCS)
    Parámetros:
      grafo: diccionario con estructura {nodo: {vecino: costo}}
      inicio: nodo inicial
      meta: nodo objetivo
    """

    # Cola de prioridad guardará tuplas (costo_total, nodo_actual, camino)
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0, inicio, [inicio]))  # costo 0, ruta [inicio]

    # Diccionario para registrar el costo mínimo encontrado para cada nodo
    costos_minimos = {inicio: 0}

    while cola_prioridad:
        costo_actual, nodo_actual, camino = heapq.heappop(cola_prioridad)

        # Si encontramos la meta, devolvemos el camino y su costo
        if nodo_actual == meta:
            return camino, costo_actual

        # Expandimos los vecinos
        for vecino, costo_arista in grafo[nodo_actual].items():
            nuevo_costo = costo_actual + costo_arista

            # Solo agregamos si no hemos visitado o si encontramos un camino más barato
            if vecino not in costos_minimos or nuevo_costo < costos_minimos[vecino]:
                costos_minimos[vecino] = nuevo_costo
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                heapq.heappush(cola_prioridad, (nuevo_costo, vecino, nuevo_camino))

    return None, float("inf")  # No se encontró camino


# ====== EJEMPLO DE USO ======
grafo = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5, 'E': 1},
    'C': {'A': 4, 'B': 2, 'E': 3},
    'D': {'B': 5, 'E': 6},
    'E': {'B': 1, 'C': 3, 'D': 6}
}

camino, costo = busqueda_costo_uniforme(grafo, 'A', 'E')
print("Camino más barato de A a E:", camino)
print("Costo total del camino:", costo)
