from collections import deque

def bfs_camino_mas_corto(grafo, inicio, meta):
    # grafo: {nodo: [vecinos]}
    # inicio: nodo inicial
    # meta: nodo objetivo al que queremos llegar

    # Cola guardará rutas completas, no solo nodos
    cola = deque()
    cola.append([inicio])  # empezamos con una ruta que solo tiene al inicio

    visitados = set()
    visitados.add(inicio)

    while cola:
        # Sacamos la ruta más vieja en la cola
        camino_actual = cola.popleft()
        nodo_actual = camino_actual[-1]  # último nodo de la ruta

        # ¿Ya llegamos?
        if nodo_actual == meta:
            return camino_actual  # esta es la ruta más corta en pasos

        # Si no llegamos, extendemos la ruta con los vecinos
        for vecino in grafo[nodo_actual]:
            if vecino not in visitados:
                visitados.add(vecino)

                # Creamos una nueva ruta que incluye al vecino
                nuevo_camino = list(camino_actual)
                nuevo_camino.append(vecino)

                cola.append(nuevo_camino)

    # Si salimos del while, no existe ruta
    return None


# ====== EJEMPLO DE USO ======
grafo_ejemplo = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "G"],
    "F": ["C"],
    "G": ["E"]
}

camino = bfs_camino_mas_corto(grafo_ejemplo, "A", "G")
print("Camino más corto de A a G:", camino)
