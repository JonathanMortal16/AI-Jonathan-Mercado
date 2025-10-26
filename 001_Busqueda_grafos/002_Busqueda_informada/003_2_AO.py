import math

def costo_de_expansion(expansion, costos_estimados):
    """
    Calcula el costo estimado de UNA expansión posible de un nodo.
    expansion = {
        "tipo": "AND" o "OR",
        "hijos": [nodo1, nodo2, ...],
        "costo": costo_inmediato (num)
    }

    costos_estimados = diccionario con el costo estimado actual de cada hijo.

    Reglas:
    - Si es OR, normalmente esa expansión tendrá un solo hijo (elegir 1 opción).
    - Si es AND, hay que sumar todos los hijos.

    Devuelve costo total estimado de usar esa expansión.
    """
    if expansion["tipo"] == "OR":
        # Para OR, asumimos que esta expansión representa elegir UN hijo.
        # Entonces costo = costo_inmediato + costo_estimado_de_ese_hijo
        hijo = expansion["hijos"][0]
        return expansion["costo"] + costos_estimados.get(hijo, math.inf)

    elif expansion["tipo"] == "AND":
        # Para AND, hay que cumplir TODOS los hijos.
        # costo total = costo_inmediato + suma(costos_hijos)
        total = expansion["costo"]
        for hijo in expansion["hijos"]:
            total += costos_estimados.get(hijo, math.inf)
        return total

    else:
        raise ValueError("Tipo de expansión inválido")


def seleccionar_mejor_expansion(nodo, grafo, costos_estimados):
    """
    De todas las expansiones posibles de 'nodo', escoge la más barata
    según los costos estimados actuales de sus hijos.

    Regresa (mejor_costo, mejor_expansion)
    """
    mejores = []
    for expansion in grafo.get(nodo, []):
        c = costo_de_expansion(expansion, costos_estimados)
        mejores.append((c, expansion))

    if not mejores:
        # Nodo sin expansiones: se asume que ya es meta o su costo
        # ya está en costos_estimados
        return (costos_estimados.get(nodo, math.inf), None)

    mejores.sort(key=lambda x: x[0])
    return mejores[0]  # regresa la tupla (costo, expansion)


def ao_star(inicio, grafo, heuristica):
    """
    AO* básico:
    - grafo: describe para cada nodo sus expansiones posibles.
      grafo[nodo] = [
        { "tipo":"OR"/"AND", "hijos":[...], "costo":numero },
        ...
      ]

    - heuristica: costo estimado inicial h(n) para cada nodo (si no está resuelto)

    Regresa:
    - costos_estimados: costo mínimo estimado para cada nodo
    - politica: qué expansión elegimos para resolver cada nodo en la mejor solución
    """

    # Inicialmente, el costo estimado de cada nodo es su heurística.
    costos_estimados = dict(heuristica)  # copia
    politica = {n: None for n in grafo.keys()}  # qué expansión elegimos al final

    # Conjunto de nodos que falta "resolver" completamente
    abiertos = {inicio}

    while abiertos:
        # 1. Elegimos un nodo "frontera" que aún no esté resuelto
        #    Heurística simple: el que tenga costo estimado menor
        nodo_actual = min(abiertos, key=lambda n: costos_estimados.get(n, math.inf))

        # 2. Expandimos ese nodo: elegimos su mejor expansión actual
        mejor_costo, mejor_exp = seleccionar_mejor_expansion(nodo_actual, grafo, costos_estimados)

        # 3. Actualizamos el costo estimado del nodo según esa mejor expansión
        costos_estimados[nodo_actual] = mejor_costo
        politica[nodo_actual] = mejor_exp

        # 4. Agregamos sus hijos (si los hay) a "abiertos"
        if mejor_exp is not None:
            for hijo in mejor_exp["hijos"]:
                if hijo in grafo:  # sólo si es un nodo que también se puede descomponer
                    abiertos.add(hijo)

        # 5. Este nodo puede que ya esté "suficientemente explicado"
        #    Si todos sus hijos ya tienen costo estable (sin infinito),
        #    podemos sacarlo de abiertos.
        listo = True
        if mejor_exp is not None:
            for hijo in mejor_exp["hijos"]:
                if costos_estimados.get(hijo, math.inf) == math.inf:
                    listo = False
                    break
        if listo:
            abiertos.remove(nodo_actual)

        # 6. Propagación hacia atrás:
        #    Cuando mejora un hijo, podría bajar el costo del padre.
        #    En AO* clásico se hace una actualización recursiva hacia arriba.
        #    Aquí lo emulamos repitiendo el ciclo mientras haya mejoras.
        #    (Nuestra heurística simple ya re-checa padres indirectamente
        #    porque seguimos iterando 'abiertos').

        # Nota: Esta es una versión simple y no "perfecta académicamente",
        # pero es suficiente para ilustrar AO* en clase.

    return costos_estimados, politica


# =========================
# EJEMPLO DE USO DE AO*
# =========================
if __name__ == "__main__":
    #
    # Vamos a modelar un problema tipo:
    #
    # Quiero resolver "Start".
    # Opciones:
    #   Opción 1 (OR): Ir directamente a "Goal". Cuesta 5.
    #   Opción 2 (AND): Hacer dos subtareas "Sub1" y "Sub2".
    #                    Eso cuesta 2 fijo más el costo de Sub1 y Sub2.
    #
    # Sub1 puede resolverse llegando a "Goal" con costo 3.
    # Sub2 puede resolverse llegando directo a "Goal" con costo 4.
    #
    # "Goal" es meta final con costo 0.
    #
    # Observa que:
    # - Start tiene una expansión tipo OR (solo una cosa)
    #   y otra expansión tipo AND (necesitas ambas subcosas).
    # - Sub1 y Sub2 son OR simples hacia Goal.
    #

    grafo = {
        "Start": [
            # Expansión 1: (OR) "Puedo simplemente ir a Goal directo"
            {"tipo": "OR", "hijos": ["Goal"], "costo": 5},

            # Expansión 2: (AND) "o puedo hacer Sub1 Y Sub2"
            {"tipo": "AND", "hijos": ["Sub1", "Sub2"], "costo": 2}
        ],

        "Sub1": [
            # Para Sub1 puedo llegar a Goal con costo 3
            {"tipo": "OR", "hijos": ["Goal"], "costo": 3}
        ],

        "Sub2": [
            # Para Sub2 puedo llegar a Goal con costo 4
            {"tipo": "OR", "hijos": ["Goal"], "costo": 4}
        ],

        # "Goal" ya no se descompone más, no tiene expansiones
        # porque ya es objetivo final.
        "Goal": []
    }

    # Heurística inicial h(n): estimación aproximada del costo de resolver cada nodo
    # Si ya estamos en Goal, costo 0.
    heuristica = {
        "Start": 10,
        "Sub1": 4,
        "Sub2": 4,
        "Goal": 0
    }

    costos_estimados, politica = ao_star("Start", grafo, heuristica)

    print("Costos estimados finales:")
    for nodo, c in costos_estimados.items():
        print(f"  {nodo}: {c}")

    print("\nPolítica (mejor expansión elegida por nodo):")
    for nodo, exp in politica.items():
        print(f"  {nodo}: {exp}")
