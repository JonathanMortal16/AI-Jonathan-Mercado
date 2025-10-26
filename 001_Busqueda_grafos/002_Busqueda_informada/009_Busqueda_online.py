import random
from collections import deque

# Representamos el mundo REAL (oculto para el agente al inicio)
# 0 = libre, 1 = pared
# S = inicio, G = meta
#
# El agente NO conoce todo esto al principio, solo conoce su celda.
#
# Ejemplo de mapa 2D tipo laberinto pequeño:
# S 0 1 0 0
# 0 0 1 0 1
# 1 0 0 0 0
# 0 1 0 1 0
# 0 0 0 1 G

mundo = [
    ['S', 0 , 1 , 0 , 0 ],
    [ 0 , 0 , 1 , 0 , 1 ],
    [ 1 , 0 , 0 , 0 , 0 ],
    [ 0 , 1 , 0 , 1 , 0 ],
    [ 0 , 0 , 0 , 1 , 'G']
]

INICIO = (0, 0)
META   = (4, 4)

FILAS = len(mundo)
COLS = len(mundo[0])

def es_valido(r, c):
    """¿La celda está dentro del mapa y no es pared?"""
    if r < 0 or r >= FILAS or c < 0 or c >= COLS:
        return False
    if mundo[r][c] == 1:
        return False
    return True

def heuristica_manhattan(a, b):
    """Distancia Manhattan entre dos celdas (r1,c1) y (r2,c2)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def vecinos_libres(r, c):
    """Vecinos alcanzables (arriba, abajo, izq, der) desde (r,c) en el mundo real."""
    pasos = [(-1,0),(1,0),(0,-1),(0,1)]
    res = []
    for dr, dc in pasos:
        nr, nc = r+dr, c+dc
        if es_valido(nr, nc):
            res.append((nr, nc))
    return res

def busqueda_online(inicio, meta, max_pasos=100):
    """
    Simulación de búsqueda online:
    - El agente empieza sin conocer el mapa completo.
    - En cada paso:
        1. Observa vecinos desde su posición actual y los agrega a su mapa interno.
        2. Elige siguiente celda "prometedora" según heurística a la meta.
        3. Se mueve.
    - Se detiene si llega a la meta o alcanza max_pasos.

    Retorna:
    - camino_recorrido: lista de posiciones visitadas por el agente en orden.
    - conocimiento: diccionario con lo que el agente aprendió del mapa.
    """

    # 'conocimiento' es lo que el agente ha descubierto del entorno
    # clave: (r,c) -> valor: {'visitado': bool, 'vecinos': [celdas alcanzables]}
    conocimiento = {}

    posicion_actual = inicio
    camino = [posicion_actual]

    for _ in range(max_pasos):

        # 1. Percibir entorno local (descubrir vecinos reales de donde estoy)
        adyacentes = vecinos_libres(*posicion_actual)
        conocimiento[posicion_actual] = {
            'visitado': True,
            'vecinos': adyacentes
        }

        # ¿Llegamos ya?
        if posicion_actual == meta:
            print("Meta alcanzada!")
            break

        # 2. Elegir siguiente movimiento
        # Estrategia simple:
        #   - Entre los vecinos alcanzables, preferimos:
        #       a) los que NO hemos visitado
        #       b) los que tengan heurística más baja hacia la meta
        candidatos = []
        for v in adyacentes:
            ya_visto = conocimiento.get(v, {'visitado': False})['visitado']
            h = heuristica_manhattan(v, meta)
            candidatos.append((h, ya_visto, v))

        if not candidatos:
            # Sin movimientos posibles -> estamos atrapados
            print("No hay más movimientos posibles, me quedé bloqueado.")
            break

        # Ordenamos:
        # 1) menor heurística (más cerca de la meta)
        # 2) preferir no visitados (False < True)
        candidatos.sort(key=lambda x: (x[0], x[1]))

        # Elegimos el mejor candidato según lo que CONOCEMOS hasta ahora
        _, _, siguiente = candidatos[0]

        # 3. Movernos físicamente (esto es la parte "online": actuamos en el mundo)
        posicion_actual = siguiente
        camino.append(posicion_actual)

    return camino, conocimiento


# ======================
# Ejemplo de uso
# ======================
if __name__ == "__main__":
    recorrido, mapa_interno = busqueda_online(INICIO, META, max_pasos=50)

    print("Camino recorrido por el agente:")
    print(recorrido)

    print("\nConocimiento aprendido (parcial) del entorno:")
    for celda, info in mapa_interno.items():
        print(celda, "->", info)
