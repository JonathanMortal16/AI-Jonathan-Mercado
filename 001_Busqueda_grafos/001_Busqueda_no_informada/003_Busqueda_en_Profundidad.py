def dfs_recursivo(grafo, nodo_actual, meta, visitados=None, camino=None):
    """
    Búsqueda en Profundidad (recursiva)
    Visita vecinos de manera recursiva hasta encontrar la meta.
    """
    if visitados is None:
        visitados = set()
    if camino is None:
        camino = []

    visitados.add(nodo_actual)
    camino = camino + [nodo_actual]

    # Si llegamos a la meta, regresamos el camino
    if nodo_actual == meta:
        return camino

    # Explorar vecinos
    for vecino in grafo[nodo_actual]:
        if vecino not in visitados:
            nuevo_camino = dfs_recursivo(grafo, vecino, meta, visitados, camino)
            if nuevo_camino:
                return nuevo_camino

    return None  # si no encuentra la meta


# ====== EJEMPLO ======
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'G'],
    'F': ['C'],
    'G': ['E']
}

camino = dfs_recursivo(grafo, 'A', 'G')
print("Camino encontrado con DFS recursivo:", camino)
