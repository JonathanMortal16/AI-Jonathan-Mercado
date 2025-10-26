def dls(grafo, nodo_actual, meta, limite, profundidad_actual=0, camino=None, visitados=None):
    """
    Búsqueda en Profundidad Limitada (Depth-Limited Search, DLS)

    Parámetros:
    - grafo: diccionario con la forma {nodo: [lista_de_vecinos]}
    - nodo_actual: nodo donde estoy parado en esta llamada
    - meta: nodo objetivo que quiero encontrar
    - limite: profundidad máxima que se permite explorar
    - profundidad_actual: cuántos pasos llevo desde el inicio
    - camino: lista que representa la ruta recorrida hasta ahora
    - visitados: conjunto de nodos ya visitados en el camino actual
                 (esto evita ciclos)

    Retorna:
    - Una lista con el camino desde el inicio hasta la meta
      si se encontró la meta DENTRO del límite de profundidad.
    - None si no se encontró.
    """

    # Inicializamos estructuras en la primera llamada
    if camino is None:
        camino = [nodo_actual]  # empezamos el camino en el nodo inicial
    if visitados is None:
        visitados = set([nodo_actual])  # marcamos el nodo inicial como visitado

    # 1. Caso base: ¿ya estamos en la meta?
    if nodo_actual == meta:
        return camino  # devolvemos el camino actual como solución

    # 2. Caso base: ¿ya alcanzamos el límite de profundidad permitido?
    if profundidad_actual == limite:
        # Ya no puedo bajar más, paro aquí SIN expandir vecinos
        return None

    # 3. Si no estoy en la meta y aún no alcancé el límite,
    #    intento explorar los vecinos (bajar más profundo)
    for vecino in grafo.get(nodo_actual, []):
        if vecino not in visitados:
            # Preparo nuevos estados para la llamada recursiva
            nuevo_camino = camino + [vecino]
            visitados.add(vecino)

            resultado = dls(
                grafo,
                vecino,
                meta,
                limite,
                profundidad_actual + 1,  # bajamos una capa más
                nuevo_camino,
                visitados
            )

            # Si en esa rama encontramos solución, la regresamos
            if resultado is not None:
                return resultado

            # IMPORTANTE:
            # Si no funcionó ese vecino, lo quitamos de visitados
            # para permitir que otros caminos paralelos lo usen.
            visitados.remove(vecino)

    # 4. Si probamos todos los vecinos y ninguno llegó a la meta dentro del límite:
    return None


# ============================================================
# EJEMPLO DE USO
# ============================================================

if __name__ == "__main__":

    # Definimos un grafo pequeño dirigido/no dirigido representado
    # como lista de adyacencia.
    #
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

    # Probamos con varios límites de profundidad
    for limite in range(0, 5):
        camino_encontrado = dls(
            grafo=grafo,
            nodo_actual=inicio,
            meta=objetivo,
            limite=limite
        )

        print("--------------------------------------------------")
        print(f"Límite de profundidad = {limite}")
        if camino_encontrado is not None:
            print("    Se encontró camino hasta la meta:")
            print("    ", camino_encontrado)
            print(f"    Profundidad usada: {len(camino_encontrado)-1} pasos")
        else:
            print("    No se encontró la meta dentro de este límite.")


# Fin del archivo 😼
