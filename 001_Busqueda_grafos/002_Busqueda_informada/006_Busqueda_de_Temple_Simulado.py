import math
import random

def f(x):
    """
    Función objetivo que queremos MAXIMIZAR.
    Puedes cambiarla.
    Esta tiene forma curva con un máximo global y otros locales,
    para que se note el efecto del algoritmo.
    """
    return -(x**2) + 20*x + 5  # misma que hemos usado: parabólica invertida


def vecino(x):
    """
    Genera un vecino cercano.
    Aquí: movemos x un pequeño paso aleatorio.
    """
    paso = random.uniform(-1.0, 1.0)  # cambiar ±1 puede controlar qué tan brusco es el salto
    return x + paso


def simulated_annealing(x_inicial, temperatura_inicial=10.0, enfriamiento=0.95, iter_por_temp=50):
    """
    Temple Simulado (Simulated Annealing) para MAXIMIZAR f(x).

    Parámetros:
    - x_inicial: estado inicial
    - temperatura_inicial: temperatura T inicial (alta = acepta más cambios malos)
    - enfriamiento: factor multiplicativo <1.0 para ir bajando T cada ciclo
    - iter_por_temp: cuántos intentos hacemos en cada nivel de temperatura

    Devuelve:
    - mejor_x_global: el mejor x visto en todo el proceso
    - mejor_valor_global: f(mejor_x_global)
    - historial: lista de (temp, x_actual, f(x_actual))
    """

    # Estado actual
    x_actual = x_inicial
    val_actual = f(x_actual)

    # Mejor global encontrado
    mejor_x_global = x_actual
    mejor_valor_global = val_actual

    T = temperatura_inicial
    historial = [(T, x_actual, val_actual)]

    # Bucle principal: vamos enfriando la temperatura
    while T > 0.0001:  # hasta que la temperatura sea prácticamente 0
        for _ in range(iter_por_temp):

            # Proponemos un nuevo candidato
            x_nuevo = vecino(x_actual)
            val_nuevo = f(x_nuevo)

            # Diferencia de calidad (porque maximizamos)
            delta = val_nuevo - val_actual

            if delta > 0:
                # Si es mejor, lo aceptamos siempre
                x_actual = x_nuevo
                val_actual = val_nuevo
            else:
                # Si es PEOR, lo aceptamos con cierta probabilidad
                # P = exp(delta / T), nota delta < 0 aquí
                prob = math.exp(delta / T)

                # random.random() da un número entre 0 y 1
                if random.random() < prob:
                    x_actual = x_nuevo
                    val_actual = val_nuevo
                # si no, nos quedamos con lo que teníamos

            # Actualizamos mejor global si aplica
            if val_actual > mejor_valor_global:
                mejor_valor_global = val_actual
                mejor_x_global = x_actual

            historial.append((T, x_actual, val_actual))

        # Enfriamos la temperatura
        T = T * enfriamiento

    return mejor_x_global, mejor_valor_global, historial


# ======================
# EJEMPLO DE USO
# ======================
if __name__ == "__main__":
    random.seed(0)  # para resultados reproducibles en pruebas

    # Probamos diferentes puntos iniciales
    for inicio in [-10, 0, 5, 15]:
        mejor_x, mejor_val, hist = simulated_annealing(
            x_inicial=inicio,
            temperatura_inicial=10.0,
            enfriamiento=0.9,
            iter_por_temp=30
        )

        print("\nInicio en x =", inicio)
        print("Mejor solución encontrada por Temple Simulado:")
        print("  x =", mejor_x, "f(x) =", mejor_val)
        print("Último estado visitado en historial:", hist[-1])
