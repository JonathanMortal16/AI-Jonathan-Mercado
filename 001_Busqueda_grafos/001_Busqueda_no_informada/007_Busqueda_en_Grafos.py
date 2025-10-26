from collections import deque

def busqueda_en_grafo_bfs(grafo, inicio, meta):
    """
    BÚSQUEDA EN GRAFO (versión BFS)
    - Explora por niveles (igual que Búsqueda en Anchura).
    - Usa un conjunto de 'visitados' para NO repetir nodos.
    - Devuelve el camino más corto en cantidad de pasos.
    
    grafo: diccionario {nodo: [lista_de_vecinos]}
    inicio: nodo inicial
    meta: nodo objetivo
    """

    # Si el inicio ya ES la meta, ya terminaste
    if inicio == meta:
        return [inicio]

    # Cola de rutas completas, no solo del nodo
    frontera = deque()
    frontera.append([inicio])

    # Conjunto de nodos que ya se visitaron
    visitados = set([inicio])

    while frontera:
        # Tomamos la ruta más vieja en la cola (BFS)
        camino_actual = frontera.popleft()
        nodo_actual = camino_actual[-1]

        # Revisamos todos los vecinos del nodo actual
        for vecino in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                # Construimos un nuevo camino extendido con ese vecino
                nuevo_camino = camino_actual + [vecino]

                # ¿Llegamos?
                if vecino == meta:
                    return nuevo_camino

                # Si no hemos llegado, seguimos explorando
                frontera.append(nuevo_camino)
                visitados.add(vecino)

    # Si la cola se vacía, no hay ruta posible
    return None


# ===================================================
# EJEMPLO DE USO
# ===================================================
if __name__ == "__main__":
    # Grafo con posibles ciclos (nota: hay conexiones de ida y vuelta)
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B', 'C'],   # <- ojo, D conecta a C y C regresa a A, eso permite ciclos
        'E': ['B', 'G'],
        'F': ['C', 'B'],   # <- F también regresa hacia B (ciclo)
        'G': ['E']
    }

    inicio = 'A'
    objetivo = 'G'

    ruta = busqueda_en_grafo_bfs(grafo, inicio, objetivo)

    print("===================================")
    print("BÚSQUEDA EN GRAFO (con visitados)")
    print("Inicio:", inicio)
    print("Meta:", objetivo)
    if ruta is not None:
        print("Ruta encontrada:", ruta)
        print("Longitud (pasos):", len(ruta) - 1)
    else:
        print("No existe ruta.")
