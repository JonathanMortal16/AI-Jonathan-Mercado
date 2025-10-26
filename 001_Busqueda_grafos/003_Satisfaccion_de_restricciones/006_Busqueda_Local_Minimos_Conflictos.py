import random

# Variables y dominios
variables = ["A", "B", "C"]
dominios = {
    "A": ["Rojo", "Verde", "Azul"],
    "B": ["Rojo", "Verde", "Azul"],
    "C": ["Rojo", "Verde", "Azul"]
}

# Vecinos (restricciones de desigualdad)
vecinos = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B"]
}

def contar_conflictos(asignacion, var, valor):
    """
    Cuenta cuántos conflictos tendría 'var = valor' con la asignación actual.
    """
    conflictos = 0
    for otro in vecinos[var]:
        if otro in asignacion and asignacion[otro] == valor:
            conflictos += 1
    return conflictos

def min_conflicts(max_iteraciones=1000):
    """
    Implementación del algoritmo de mínimos conflictos.
    max_iteraciones: límite para evitar bucles infinitos.
    """

    # 1. Asignación inicial aleatoria
    asignacion = {v: random.choice(dominios[v]) for v in variables}

    for paso in range(max_iteraciones):
        # 2. Calcular todas las variables en conflicto
        conflicivas = []
        for v in variables:
            for vecino in vecinos[v]:
                if asignacion[v] == asignacion[vecino]:
                    conflicivas.append(v)
                    break  # ya sabemos que v está en conflicto

        # Si no hay conflictos -> solución encontrada
        if not conflicivas:
            print(f"Solución encontrada en {paso} pasos:")
            return asignacion

        # 3. Elegir una variable conflictiva al azar
        var = random.choice(conflicivas)

        # 4. Escoger el valor del dominio que minimiza los conflictos
        mejor_valor = min(dominios[var], key=lambda val: contar_conflictos(asignacion, var, val))

        # 5. Actualizar la variable con el valor menos conflictivo
        asignacion[var] = mejor_valor

    # Si no encontramos solución tras todas las iteraciones
    print("No se encontró solución dentro del límite de iteraciones.")
    return asignacion

# Ejecutamos el algoritmo
solucion = min_conflicts()

print(solucion)
