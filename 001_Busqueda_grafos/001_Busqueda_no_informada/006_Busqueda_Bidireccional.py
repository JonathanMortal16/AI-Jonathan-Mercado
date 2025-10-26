from collections import deque

def reconstruir_camino(padres_inicio, padres_meta, punto_encuentro, inicio, meta):
    """
    Reconstruye el camino completo usando:
    - padres_inicio: diccionario {nodo: padre} desde el inicio
    - padres_meta:   diccionario {nodo: padre} desde la meta (al revés)
    - punto_encuentro: nodo donde se cruzaron ambas búsquedas
    """

    # Reconstruir desde el punto de encuentro hacia el inicio
    camino_desde_inicio = []
    actual = punto_encuentro
    while actual is not None:
        camino_desde_inicio.append(actual)
        actual = padres_inicio.get(actual, None)
    camino_desde_inicio.reverse()  # porque lo armamos hacia atrás

    # Reconstruir desde el punto de encuentro hacia la meta
    camino_hacia_meta = []
    actual = padres_meta.get(punto_encuentro, None)  # importante: saltamos el punto_encuentro mismo
    while actual is not None:
        camino_hacia_meta.append(actual)
        actual = padres_meta.get(actual, None)

    # Unimos las dos mitades
    camino_total = camino_desde_inicio + camino_hacia_meta
    return camino_total


def busqueda_bidireccional(grafo, inicio, meta):
    """
    Búsqueda Bidireccional en un grafo no ponderado.
    Objetivo: encontrar el camino más corto en número de saltos.

    Estrategia:
    - BFS desde 'inicio'
    - BFS desde 'meta'
    - Parar cuando ambas búsquedas se tocan
    """

    if inicio == meta:
        return [inicio]  # caso trivial

    # Colas tipo BFS
    cola_inicio = deque([inicio])
    cola_meta   = deque([meta])

    # Visitados por cada lado
    visitados_inicio = {inicio}
    visitados_meta   = {meta}

    # "padres" para reconstruir ruta
    # padres_inicio[x] = de qué nodo llegué a x (yendo desde inicio)
    # padres_meta[x]   = de qué nodo llegué a x (yendo desde meta)
    padres_inicio = {inicio: None}
    padres_meta   = {meta: None}

    while cola_inicio and cola_meta:
        # --- Paso 1: expandimos desde el lado del inicio ---
        if cola_inicio:
            actual_inicio = cola_inicio.popleft()

            for vecino in grafo.get(actual_inicio, []):
                if vecino not in visitados_inicio:
                    visitados_inicio.add(vecino)
                    padres_inicio[vecino] = actual_inicio
                    cola_inicio.append(vecino)

                    # ¿Este vecino ya fue visto desde el otro lado?
                    if vecino in visitados_meta:
                        # Se encontraron las búsquedas
                        return reconstruir_camino(
                            padres_inicio, padres_meta, vecino, inicio, meta
                        )

        # --- Paso 2: expandimos desde el lado de la meta ---
        if cola_meta:
            actual_meta = cola_meta.popleft()

            for vecino in grafo.get(actual_meta, []):
                if vecino not in visitados_meta:
                    visitados_meta.add(vecino)
                    padres_meta[vecino] = actual_meta
                    cola_meta.append(vecino)

                    # ¿Este vecino ya fue visto desde el lado inicio?
                    if vecino in visitados_inicio:
                        return reconstruir_camino(
                            padres_inicio, padres_meta, vecino, inicio, meta
                        )

    # Si salimos del while sin return, no existe conexión
    return None


# =========================
# PRUEBA / DEMO
# =========================
if __name__ == "__main__":
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'G'],
        'F': ['C'],
        'G': ['E']
    }

    inicio = 'A'
    meta = 'G'

    resultado = busqueda_bidireccional(grafo, inicio, meta)

    print("=======================================")
    print("BÚSQUEDA BIDIRECCIONAL")
    print("Inicio:", inicio)
    print("Meta:", meta)
    if resultado is not None:
        print("Camino más corto encontrado:", resultado)
        print("Número de pasos:", len(resultado) - 1)
    else:
        print("No hay camino entre inicio y meta.")
