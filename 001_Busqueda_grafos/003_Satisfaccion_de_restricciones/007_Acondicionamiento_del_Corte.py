import itertools

# ---- Definición del CSP ----

variables = ["A", "B", "C", "D"]

dominios_globales = {
    "A": ["Rojo", "Verde", "Azul"],
    "B": ["Rojo", "Verde", "Azul"],
    "C": ["Rojo", "Verde", "Azul"],
    "D": ["Rojo", "Verde", "Azul"]
}

# Restricciones binarias: X != Y
restricciones = [
    ("A", "B"),
    ("B", "C"),
    ("C", "D"),
    ("D", "A"),
    ("B", "D")  # esta arista extra hace el grafo más "cíclico"
]

# Conjunto de corte: las variables que vamos a fijar primero
cutset = ["B"]  # en un caso más complejo, podrían ser ["B","C"]


def es_consistente_parcial(asignacion, var, valor):
    """
    Verifica que asignar 'valor' a 'var' no rompe restricciones
    con lo que ya está en 'asignacion'.
    """
    for (x, y) in restricciones:
        # Para cada restricción X != Y:
        if x == var and y in asignacion:
            if asignacion[y] == valor:
                return False
        if y == var and x in asignacion:
            if asignacion[x] == valor:
                return False
    return True


def backtracking_resto(asignacion_parcial):
    """
    Backtracking normal SOLO para las variables que no están todavía asignadas.
    Esto se corre DESPUÉS de haber fijado las variables del cutset.
    """

    # Si ya asigné todas las variables, terminé
    if len(asignacion_parcial) == len(variables):
        return asignacion_parcial

    # Buscar siguiente variable sin asignar
    for v in variables:
        if v not in asignacion_parcial:
            var_siguiente = v
            break

    # Intentar cada valor de su dominio global
    for valor in dominios_globales[var_siguiente]:
        if es_consistente_parcial(asignacion_parcial, var_siguiente, valor):
            asignacion_parcial[var_siguiente] = valor
            resultado = backtracking_resto(asignacion_parcial)
            if resultado is not None:
                return resultado
            del asignacion_parcial[var_siguiente]

    # Si ninguno funcionó, fallo
    return None


def condicionamiento_del_corte():
    """
    Intenta resolver el CSP usando acondicionamiento del corte.
    1. Genera todas las combinaciones posibles para las variables del cutset.
    2. Para cada combinación, intenta resolver el resto con backtracking_resto.
    """

    # Lista de dominios para cada variable del cutset, en orden
    listas_dom = [dominios_globales[v] for v in cutset]

    # Producto cartesiano: todas las asignaciones posibles del cutset
    for valores_cutset in itertools.product(*listas_dom):
        # Construimos una asignación parcial con el cutset fijado
        asignacion_inicial = {}
        valido = True

        # Asignamos cada variable del cutset con su valor correspondiente
        for var_cs, val_cs in zip(cutset, valores_cutset):
            # Checar consistencia interna conforme vamos agregando
            if es_consistente_parcial(asignacion_inicial, var_cs, val_cs):
                asignacion_inicial[var_cs] = val_cs
            else:
                valido = False
                break

        if not valido:
            # Esta combinación del cutset ya viola restricciones entre ellas
            continue

        # Intentar resolver el resto con backtracking
        solucion_completa = backtracking_resto(asignacion_inicial.copy())
        if solucion_completa is not None:
            return solucion_completa  # ¡Listo!

    # Si ninguna combinación del cutset funcionó:
    return None


# Ejecutar
solucion = condicionamiento_del_corte()

if solucion is not None:
    print("Solución encontrada con Acondicionamiento del Corte:")
    for v in variables:
        print(f"{v} = {solucion[v]}")
else:
    print("No se encontró solución con este cutset.")
