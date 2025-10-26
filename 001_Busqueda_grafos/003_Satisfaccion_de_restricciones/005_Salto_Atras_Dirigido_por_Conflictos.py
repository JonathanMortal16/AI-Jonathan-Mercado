# -------------------------------------------------
# Salto Atrás Dirigido por Conflictos (CBJ)
# Ejemplo: Coloreo de Mapa
#
# Idea: igual que backtracking, pero cuando se detecta
# un conflicto, el algoritmo analiza qué variables
# causaron el fallo y salta directamente hacia ellas.
# -------------------------------------------------

variables = ["A", "B", "C"]
dominios = {
    "A": ["Rojo", "Verde", "Azul"],
    "B": ["Rojo", "Verde", "Azul"],
    "C": ["Rojo", "Verde", "Azul"]
}

# Vecindad (restricciones de desigualdad)
vecinos = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B"]
}

def es_consistente(asignacion, var, valor):
    """Verifica si asignar 'valor' a 'var' respeta todas las restricciones."""
    for otro in vecinos[var]:
        if otro in asignacion and asignacion[otro] == valor:
            return False
    return True

def conflict_directed_backjump(asignacion, variable_idx, conflictos):
    """
    Algoritmo recursivo CBJ.
    asignacion: dict actual de asignaciones válidas.
    variable_idx: índice de la variable actual.
    conflictos: diccionario que guarda los conjuntos de conflicto.
    """

    # Caso base: todas las variables asignadas
    if variable_idx == len(variables):
        return True, conflictos

    var = variables[variable_idx]
    for valor in dominios[var]:
        if es_consistente(asignacion, var, valor):
            # Asignación válida, probamos siguiente variable
            asignacion[var] = valor
            exito, conflictos = conflict_directed_backjump(asignacion, variable_idx + 1, conflictos)
            if exito:
                return True, conflictos
            # Si hubo conflicto más adelante, revisamos si debemos saltar atrás
            if conflictos.get(variables[variable_idx + 1], set()) - {var}:
                # Si el conflicto no involucra a esta variable, se mantiene
                pass
            else:
                # Si sí está involucrada, agregamos al conjunto de conflicto
                conflictos[var] = conflictos.get(var, set()).union(
                    conflictos.get(variables[variable_idx + 1], set())
                )
        else:
            # Si hay conflicto, agregamos al conjunto de conflicto actual
            conflictos[var] = conflictos.get(var, set())
            for otro in vecinos[var]:
                if otro in asignacion:
                    conflictos[var].add(otro)

    # Si probamos todos los valores y fallamos → devolvemos el conjunto de conflicto
    if var in conflictos and len(conflictos[var]) > 0:
        # "Saltamos" hacia la variable más reciente involucrada en el conflicto
        ultima_conflictiva = max([variables.index(v) for v in conflictos[var]])
        return False, conflictos  # se volverá a esa variable
    return False, conflictos

# -------------------- Ejecución --------------------
asignacion = {}
conflictos = {}

exito, conflictos = conflict_directed_backjump(asignacion, 0, conflictos)

if exito:
    print("Solución encontrada con CBJ:")
    print(asignacion)
else:
    print("No hay solución.")
    print("Conflictos detectados:", conflictos)
