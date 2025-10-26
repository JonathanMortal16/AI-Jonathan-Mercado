# Definimos las variables del problema:
variables = ["A", "B", "C"]

# Definimos el dominio de cada variable:
dominios = {
    "A": ["Rojo", "Verde", "Azul"],
    "B": ["Rojo", "Verde", "Azul"],
    "C": ["Rojo", "Verde", "Azul"]
}

# Definimos las restricciones binarias de desigualdad entre vecinos.
# Cada tupla (X, Y) significa "X debe ser distinto de Y".
restricciones_vecinos = [
    ("A", "B"),
    ("B", "C"),
    ("A", "C")
]

def es_consistente(asignacion_parcial, var_actual, valor_actual):
    """
    Revisa si asignar 'valor_actual' a 'var_actual' rompe alguna restricción
    con lo que ya está asignado.
    
    asignacion_parcial: dict con asignaciones actuales, ej: {"A":"Rojo", "B":"Verde"}
    var_actual: la variable que estamos intentando asignar ahora, ej: "C"
    valor_actual: el valor que queremos probar, ej: "Azul"
    """

    # Recorremos todas las restricciones del tipo X != Y
    for (x, y) in restricciones_vecinos:
        # Caso 1: var_actual es x, checar contra y
        if x == var_actual and y in asignacion_parcial:
            # Si el vecino ya tiene el mismo color, NO es consistente
            if asignacion_parcial[y] == valor_actual:
                return False

        # Caso 2: var_actual es y, checar contra x
        if y == var_actual and x in asignacion_parcial:
            if asignacion_parcial[x] == valor_actual:
                return False

    # Si no violó ninguna restricción, es consistente
    return True

def backtracking(asignacion_parcial):
    """
    Intenta completar la asignación de todas las variables usando backtracking.
    - asignacion_parcial es un diccionario con las variables ya asignadas.
    - Si se logra asignar TODO de forma consistente, regresa esa asignación.
    - Si no hay solución, regresa None.
    """

    # 1. Si ya asignamos TODAS las variables, terminamos.
    if len(asignacion_parcial) == len(variables):
        return asignacion_parcial

    # 2. Elegimos una variable NO asignada todavía.
    #    (versión simple: toma la primera que falte)
    for var in variables:
        if var not in asignacion_parcial:
            var_siguiente = var
            break

    # 3. Probamos cada valor posible del dominio de esa variable.
    for valor in dominios[var_siguiente]:
        if es_consistente(asignacion_parcial, var_siguiente, valor):
            # Si es consistente, asignamos temporalmente
            asignacion_parcial[var_siguiente] = valor

            # Repetimos recursivamente
            resultado = backtracking(asignacion_parcial)
            if resultado is not None:
                return resultado  # encontramos solución válida

            # Si no funcionó, quitamos la asignación (backtrack)
            del asignacion_parcial[var_siguiente]

    # 4. Si probamos todos los valores y ninguno funcionó, no hay solución
    return None

# Ejecutamos el solver:
solucion = backtracking({})

# Mostramos la solución encontrada
if solucion is not None:
    print("Solución encontrada:")
    for var in variables:
        print(f"{var} = {solucion[var]}")
else:
    print("No existe solución válida.")
