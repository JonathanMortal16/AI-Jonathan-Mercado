def dls(grafo, nodo_actual, meta, limite, profundidad_actual=0, camino=None, visitados=None):
    """
    DLS = Depth-Limited Search = Búsqueda en Profundidad Limitada.
    Esta función intenta encontrar 'meta' desde 'nodo_actual'
    sin pasar de 'limite' de profundidad.

    Retorna:
        - una lista con el camino si encuentra la meta
        - None si no se pudo dentro de este límite
    """

    # Inicialización al entrar por primera vez
    if camino is None:
        camino = [nodo_actual]
    if visitados is None:
        visitados = set([nodo_actual])

    # Caso 1: ya estoy en la meta
    if nodo_actual == meta:
        return camino

    # Caso 2: llegué al límite de profundidad permitido
    if profundidad_actual == limite:
        return None

    # Caso 3: sigo explorando hijos
    for vecino in grafo.get(nodo_actual, []):
        if vecino not in visitados:
            nuevo_camino = camino + [vecino]
            visitados.add(vecino)

            resultado = dls(
                grafo,
                vecino,
                meta,
                limite,
                profundidad_actual + 1,  # bajamos una capa
                nuevo_camino,
                visitados
            )

            if resultado is not None:
                return resultado

            # backtrack: libero ese nodo para otras ramas
            visitados.remove(vecino)

    return None  # no se encontró nada útil en esta rama


def busqueda_profundidad_iterativa(grafo, inicio, meta, limite_maximo):
    """
    Búsqueda en Profundidad Iterativa (IDDFS)
    Va aumentando el límite de profundidad paso a paso.

    Parámetros:
        grafo: diccionario {nodo: [vecinos]}
        inicio: nodo inicial
        meta: nodo objetivo
        limite_maximo: hasta qué profundidad máxima vamos a intentar

    Retorna:
        - el camino encontrado (lista de nodos) si se encontró
        - None si no se halló la meta hasta limite_maximo
    """

    for limite in range(limite_maximo + 1):
        print(f"Probando con límite de profundidad = {limite} ...")
        resultado = dls(
            grafo=grafo,
            nodo_actual=inicio,
            meta=meta,
            limite=limite
        )

        if resultado is not None:
            print(f">>> Se encontró solución con límite = {limite}")
            return resultado

    # Si llegamos aquí, no se encontró dentro del límite máximo
    return None


# ============================================================
# EJEMPLO DE USO
# ============================================================

if __name__ == "__main__":
    # Definimos un grafo sencillo dirigido/no dirigido con adyacencias
    # A conecta a B y C
    # B conecta a D y E
    # E conecta a G
    # C conecta a F


    grafo = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['G'],
        'F': [],
        'G': []
    }

    inicio = 'A'
    objetivo = 'G'

    # Límite máximo: hasta qué tan profundo estamos dispuestos a buscar.
    # Si lo pones muy bajo, tal vez no alcance la meta.
    # Si lo pones muy alto, explora más niveles.
    limite_maximo = 5

    camino = busqueda_profundidad_iterativa(grafo, inicio, objetivo, limite_maximo)

    print("===========================================")
    if camino is not None:
        print("Camino encontrado:", camino)
        print("Profundidad usada:", len(camino) - 1, "pasos")
    else:
        print("No se encontró la meta dentro del límite máximo.")
