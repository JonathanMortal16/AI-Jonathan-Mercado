variables = ["A", "B", "C"]

# Dominio inicial compartido
dominio_inicial = ["Rojo", "Verde", "Azul"]

# Grafo de vecindad (quién es vecino de quién)
vecinos = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B"]
}

def forward_checking(asignacion_actual, dominios_actuales):
    """
    Esta función hace la parte recursiva del algoritmo con comprobación hacia delante.

    asignacion_actual: dict con asignaciones hechas hasta ahora, ej {"A": "Rojo"}
    dominios_actuales: dict con los dominios POSIBLES restantes para cada variable
                       ej {"A":["Rojo"], "B":["Verde","Azul"], "C":["Verde","Azul"]}
                       Nota: para variables ya asignadas, su dominio se reduce a [valor asignado]
    """

    # Caso base: si TODAS las variables ya están asignadas -> solución completa
    if len(asignacion_actual) == len(variables):
        return asignacion_actual

    # 1. Elegimos una variable sin asignar todavía
    var_siguiente = None
    for v in variables:
        if v not in asignacion_actual:
            var_siguiente = v
            break

    # 2. Probamos cada valor posible para esa variable
    for valor in dominios_actuales[var_siguiente]:

        # Hacemos copias (porque vamos a modificar y luego quizá revertir)
        asignacion_nueva = asignacion_actual.copy()
        dominios_nuevos = {v: dominios_actuales[v][:] for v in dominios_actuales}

        # Asignamos var_siguiente = valor
        asignacion_nueva[var_siguiente] = valor
        dominios_nuevos[var_siguiente] = [valor]  # su dominio ya queda fijo

        # 3. *** Comprobación Hacia Delante ***
        # Recortamos los dominios de las variables no asignadas.
        consistente = True
        for vecino in vecinos[var_siguiente]:
            # Sólo nos interesa reducir dominios de los que aún NO están asignados
            if vecino not in asignacion_nueva:
                # Quitamos del dominio de 'vecino' el valor que acabamos de fijar
                if valor in dominios_nuevos[vecino]:
                    dominios_nuevos[vecino].remove(valor)

                # Si algún vecino se quedó sin valores posibles,
                # esta asignación NO sirve -> marcamos inconsistente
                if len(dominios_nuevos[vecino]) == 0:
                    consistente = False
                    break

        # Si sigue siendo consistente después de recortar dominios, seguimos recursivamente
        if consistente:
            resultado = forward_checking(asignacion_nueva, dominios_nuevos)
            if resultado is not None:
                return resultado  # encontramos solución válida

        # Si no fue consistente o la recursión falló, probamos el siguiente valor
        # (no necesitamos "deshacer" manualmente porque usamos copias)

    # Si ningún valor funcionó para esta variable, no hay solución por esta rama
    return None


# --- Preparar estructuras iniciales e invocar el solver ---

# Al inicio, ninguna variable está asignada
asignacion_inicial = {}

# Cada variable empieza con el dominio completo
dominios_iniciales = {v: dominio_inicial[:] for v in variables}

solucion = forward_checking(asignacion_inicial, dominios_iniciales)

# Mostrar resultado
if solucion is not None:
    print("Solución encontrada con Comprobación Hacia Delante:")
    for v in variables:
        print(f"{v} = {solucion[v]}")
else:
    print("No hay solución posible.")
