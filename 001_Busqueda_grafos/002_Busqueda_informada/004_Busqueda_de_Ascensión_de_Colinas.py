import random

def f(x):
    """
    Función objetivo que queremos MAXIMIZAR.
    Aquí puedes poner lo que quieras optimizar.
    Ejemplo: una curva con varios máximos locales.
    """
    # Ejemplo con una función no-lineal con varios 'cerros'
    # mientras más grande regrese, mejor es x
    return -(x**2) + 20*x + 5  # es una parábola invertida


def generar_vecinos(x):
    """
    Genera vecinos 'cercanos' al estado actual.
    Aquí voy a decir que los vecinos son x-1 y x+1.
    """
    return [x - 1, x + 1]


def hill_climbing(x_inicial, max_iter=100):
    """
    Búsqueda de Ascensión de Colinas (Hill Climbing básico).
    - Empieza en x_inicial.
    - En cada paso, se mueve al mejor vecino si mejora la función f(x).
    - Se detiene si ya no encuentra mejora.

    Devuelve:
    - mejor_x: el valor final de x
    - mejor_f: el valor f(x) correspondiente
    - historial: lista de (x, f(x)) para ver cómo fue subiendo
    """

    actual = x_inicial
    valor_actual = f(actual)

    historial = [(actual, valor_actual)]

    for _ in range(max_iter):
        vecinos = generar_vecinos(actual)

        # Evaluamos todos los vecinos
        mejor_vecino = actual
        mejor_valor = valor_actual

        for v in vecinos:
            val_v = f(v)
            # Buscamos estrictamente mejor
            if val_v > mejor_valor:
                mejor_vecino = v
                mejor_valor = val_v

        # Si ningún vecino mejora, paramos (máximo local alcanzado)
        if mejor_valor <= valor_actual:
            break

        # Si encontramos un vecino mejor, nos movemos allí
        actual = mejor_vecino
        valor_actual = mejor_valor
        historial.append((actual, valor_actual))

    return actual, valor_actual, historial


# ======================
# EJEMPLO DE USO
# ======================
if __name__ == "__main__":
    # Probamos empezar desde diferentes puntos
    for inicio in [ -10, 0, 5, 15 ]:
        mejor_x, mejor_f, hist = hill_climbing(inicio)
        print("\nInicio en x =", inicio)
        print("Máximo local encontrado:")
        print("  x =", mejor_x, "f(x) =", mejor_f)
        print("Historial de mejoras:", hist)
