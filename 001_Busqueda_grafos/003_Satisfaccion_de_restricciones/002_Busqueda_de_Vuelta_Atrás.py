# Variables del problema (regiones del mapa)
variables = ["A", "B", "C"]

# Dominio de cada variable (colores permitidos)
dominios = {
    "A": ["Rojo", "Verde", "Azul"],
    "B": ["Rojo", "Verde", "Azul"],
    "C": ["Rojo", "Verde", "Azul"]
}

# Restricciones binarias:
# Cada par (X,Y) significa "X y Y no pueden tener el mismo valor"
restricciones_vecinos = [
    ("A", "B"),
    ("B", "C"),
    ("A", "C")
]

def es_consistente(asignacion_actual, var, valor):
    """
    Revisa si asignar 'valor' a 'var' respeta TODAS las
    restricciones con las variables que ya están asignadas.

    asignacion_actual: diccionario parcial, ej: {"A": "Rojo", "B": "Verde"}
    var: la variable que estoy intentando asignar ahorita, ej: "C"
    valor: el valor que quiero darle a esa variable, ej: "Azul"
    """

    # Recorremos las restricciones binarias (X != Y)
    for (x, y) in restricciones_vecinos:

        # Caso 1: si la restricción es entre var y otra variable ya asignada
        if x == var and y in asignacion_actual:
            # Si la otra variable tiene el mismo valor → conflicto
            if asignacion_actual[y] == valor:
                return False

        if y == var and x in asignacion_actual:
            if asignacion_actual[x] == valor:
                return False

    # Si no rompimos ninguna restricción, es consistente
    return True

def seleccionar_variable_no_asignada(asignacion_actual):
    """
    Estrategia simple:
    Regresa la primera variable que aún no esté en la asignación.
    (Hay estrategias más inteligentes, pero esta es la más clara.)
    """
    for v in variables:
        if v not in asignacion_actual:
            return v
    return None  # ya no hay variables disponibles

def backtracking(asignacion_actual):
    """
    Algoritmo de Búsqueda de Vuelta Atrás.
    Intenta completar una asignación consistente para todas las variables.

    asignacion_actual: diccionario con las variables ya asignadas.
                       Ej: {"A":"Rojo", "B":"Verde"}

    Retorna:
    - Un diccionario con solución completa si la encuentra.
    - None si no hay solución bajo las decisiones actuales.
    """

    # Caso base: si ya asignamos TODAS las variables, estamos listos
    if len(asignacion_actual) == len(variables):
        return asignacion_actual

    # 1. Elegir una variable pendiente
    var = seleccionar_variable_no_asignada(asignacion_actual)

    # 2. Probar cada valor posible para esa variable
    for valor in dominios[var]:

        # 2a. Verificamos si esta asignación respeta las restricciones
        if es_consistente(asignacion_actual, var, valor):
            # "Asignamos" tentativamente
            asignacion_actual[var] = valor

            # 2b. Seguimos con el resto de variables
            resultado = backtracking(asignacion_actual)
            if resultado is not None:
                # Si el resultado NO es None, significa que encontramos
                # una solución completa y válida. La regresamos.
                return resultado

            # 2c. Si no funcionó, quitamos la asignación (VUELTA ATRÁS)
            del asignacion_actual[var]

    # 3. Si ningún valor funcionó para esta variable, no hay solución aquí
    return None

# Ejecutamos el algoritmo
solucion = backtracking({})

# Mostramos resultado
if solucion is not None:
    print("Solución encontrada con Búsqueda de Vuelta Atrás:")
    for v in variables:
        print(f"{v} = {solucion[v]}")
else:
    print("No hay solución posible.")
