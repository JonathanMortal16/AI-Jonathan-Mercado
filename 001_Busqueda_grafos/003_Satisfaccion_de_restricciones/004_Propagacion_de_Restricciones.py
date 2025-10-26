from collections import deque

# Variables del problema
variables = ["A", "B", "C"]

# Dominios iniciales
dominios = {
    "A": ["Rojo", "Verde", "Azul"],
    "B": ["Rojo", "Verde", "Azul"],
    "C": ["Rojo", "Verde", "Azul"]
}

# Vecindad (restricciones binarias: vecinos ≠ mismo color)
vecinos = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B"]
}

def consistente(x, y, valor_x, valor_y):
    """
    Devuelve True si los valores valor_x y valor_y son compatibles
    bajo la restricción 'x != y'.
    """
    return valor_x != valor_y

def ac3(dominios, vecinos):
    """
    Algoritmo AC-3 de propagación de restricciones.
    Reduce dominios hasta alcanzar consistencia de arco.

    dominios: dict con los dominios de cada variable
    vecinos: dict con las relaciones entre variables
    """

    # Cola de arcos (pares de variables relacionadas)
    cola = deque()
    for x in variables:
        for y in vecinos[x]:
            cola.append((x, y))

    while cola:
        (x, y) = cola.popleft()

        if revisar_arco(x, y, dominios):
            # Si se eliminó algún valor del dominio de x
            if len(dominios[x]) == 0:
                return False  # inconsistencia detectada

            # Añadimos de nuevo los arcos (z, x) para todos los vecinos de x (menos y)
            for z in vecinos[x]:
                if z != y:
                    cola.append((z, x))

    return True  # los dominios son consistentes

def revisar_arco(x, y, dominios):
    """
    Revisa el arco (x, y): elimina valores de dom(x)
    que no tienen soporte en dom(y).
    Devuelve True si se eliminó al menos un valor.
    """

    eliminado = False
    for valor_x in dominios[x][:]:  # copia del dominio
        # ¿Existe al menos un valor_y que mantenga la restricción?
        if not any(consistente(x, y, valor_x, valor_y) for valor_y in dominios[y]):
            dominios[x].remove(valor_x)
            eliminado = True
    return eliminado


# -------------------- Prueba del algoritmo --------------------

print("Dominios iniciales:")
for v in variables:
    print(f"{v}: {dominios[v]}")

resultado = ac3
