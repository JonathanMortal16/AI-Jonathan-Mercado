import random

def f(x):
    """
    Función objetivo que queremos MAXIMIZAR.
    Puedes cambiarla si quieres probar otro caso.
    """
    # Ejemplo con varios máximos locales
    return -(x**2) + 20*x + 5


def generar_vecinos(x, n_vecinos=3):
    """
    Genera 'n_vecinos' estados cercanos a x.
    """
    vecinos = []
    for _ in range(n_vecinos):
        paso = random.uniform(-2, 2)  # variación aleatoria pequeña
        vecinos.append(x + paso)
    return vecinos


def local_beam_search(k=3, max_iter=50):
    """
    Implementación simple de Búsqueda de Haz Local.
    
    Parámetros:
    - k: número de soluciones activas (tamaño del haz)
    - max_iter: número máximo de iteraciones

    Devuelve:
    - mejor_solucion: el mejor x encontrado
    - mejor_valor: f(x) correspondiente
    - historial: lista de mejores soluciones por iteración
    """

    # Paso 1: Inicializamos k soluciones aleatorias
    soluciones = [random.uniform(-10, 20) for _ in range(k)]
    historial = []

    for iteracion in range(max_iter):
        # Evaluamos todas las soluciones actuales
        valores = [(x, f(x)) for x in soluciones]

        # Ordenamos de mejor a peor
        valores.sort(key=lambda x: x[1], reverse=True)

        mejor_actual = valores[0]
        historial.append(mejor_actual)

        # Mostramos progreso opcional
        # print(f"Iteración {iteracion}: Mejor x = {mejor_actual[0]:.3f}, f(x) = {mejor_actual[1]:.3f}")

        # Paso 2: Generamos todos los vecinos de las k soluciones actuales
        todos_vecinos = []
        for x, _ in valores:
            todos_vecinos.extend(generar_vecinos(x, n_vecinos=3))  # 3 vecinos por solución

        # Paso 3: Evaluamos a todos los vecinos
        candidatos = [(x, f(x)) for x in todos_vecinos]

        # Paso 4: Escogemos las k mejores soluciones globales (entre todas)
        candidatos.sort(key=lambda x: x[1], reverse=True)
        soluciones = [x for x, _ in candidatos[:k]]

    # Al final, tomamos la mejor solución encontrada
    mejor_solucion, mejor_valor = max(historial, key=lambda x: x[1])

    return mejor_solucion, mejor_valor, historial


# ======================
# EJEMPLO DE USO
# ======================
if __name__ == "__main__":
    random.seed(0)

    mejor_x, mejor_val, hist = local_beam_search(k=4, max_iter=20)

    print("Mejor solución encontrada por Búsqueda de Haz Local:")
    print("  x =", round(mejor_x, 3))
    print("  f(x) =", round(mejor_val, 3))
