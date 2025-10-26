import random
from collections import deque

def f(x):
    """
    Función objetivo que queremos MAXIMIZAR.
    Puedes cambiarla para representar el problema real.
    """
    # Ejemplo con varias subidas y bajadas (para que haya trampas locales):
    # Esto crea como "cerros" y "valles".
    return -(x**2) + 20*x + 5  # misma de antes para mantenerlo claro


def generar_vecinos(x):
    """
    Genera vecinos cercanos al estado actual.
    Aquí: x-1 y x+1
    """
    return [x - 1, x + 1]


def tabu_search(x_inicial, max_iter=50, tabu_tam=5):
    """
    Implementación sencilla de Búsqueda Tabú.
    
    Parámetros:
    - x_inicial: estado inicial
    - max_iter: cuántos pasos intentamos mejorar / explorar
    - tabu_tam: tamaño máximo de la lista tabú (memoria reciente)

    Devuelve:
    - mejor_global_x: el mejor estado encontrado en todo el proceso
    - mejor_global_val: el valor f(x) de ese mejor estado
    - historial: lista de (x_actual, f(x_actual)) por iteración
    """

    # Estado actual
    actual_x = x_inicial
    actual_val = f(actual_x)

    # Mejor solución global encontrada hasta ahora
    mejor_global_x = actual_x
    mejor_global_val = actual_val

    # Lista tabú (usamos deque para manejar tamaño fijo)
    tabu = deque()
    tabu.append(actual_x)

    historial = [(actual_x, actual_val)]

    for _ in range(max_iter):
        vecinos = generar_vecinos(actual_x)

        # Evaluamos a todos los vecinos y escogemos el "mejor permitido"
        mejor_vecino_x = None
        mejor_vecino_val = None

        for v in vecinos:
            val_v = f(v)

            # Regla Tabú:
            # - Si v está en tabu, en principio NO lo elegimos...
            # - PERO si mejora el mejor_global_val, aplicamos criterio de aspiración
            permitido = (v not in tabu) or (val_v > mejor_global_val)

            if not permitido:
                continue

            # Elegimos el mejor vecino permitido (maximizamos f)
            if (mejor_vecino_x is None) or (val_v > mejor_vecino_val):
                mejor_vecino_x = v
                mejor_vecino_val = val_v

        # Si no encontramos ningún vecino permitido, rompemos (atascados)
        if mejor_vecino_x is None:
            break

        # Nos movemos al mejor vecino permitido (aunque pueda ser peor que el actual)
        actual_x = mejor_vecino_x
        actual_val = mejor_vecino_val

        # Guardamos en historial
        historial.append((actual_x, actual_val))

        # Actualizamos mejor global si aplica
        if actual_val > mejor_global_val:
            mejor_global_val = actual_val
            mejor_global_x = actual_x

        # Actualizamos la lista tabú
        tabu.append(actual_x)
        if len(tabu) > tabu_tam:
            tabu.popleft()

    return mejor_global_x, mejor_global_val, historial


# ======================
# EJEMPLO DE USO
# ======================
if __name__ == "__main__":
    # Probamos varias corridas con diferentes puntos iniciales
    for inicio in [-10, 0, 5, 15]:
        mejor_x, mejor_val, hist = tabu_search(inicio, max_iter=30, tabu_tam=5)

        print("\nInicio en x =", inicio)
        print("Mejor global encontrado por Búsqueda Tabú:")
        print("  x =", mejor_x, "f(x) =", mejor_val)

        print("Historial de visita (x, f(x)):")
        print(hist)
