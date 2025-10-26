import random

# ----------------------------
# Función objetivo (fitness)
# ----------------------------
def f(x):
    """
    Función que queremos MAXIMIZAR.
    Puedes cambiarla a lo que necesites.
    """
    return -(x**2) + 20*x + 5  # misma que antes, para comparar resultados


# ----------------------------
# Parámetros del algoritmo
# ----------------------------
TAM_POBLACION = 10
GENERACIONES = 30
PROB_MUTACION = 0.2
LIM_INFERIOR = -10
LIM_SUPERIOR = 20


# ----------------------------
# Funciones auxiliares
# ----------------------------
def generar_individuo():
    """Crea un individuo aleatorio dentro del rango permitido."""
    return random.uniform(LIM_INFERIOR, LIM_SUPERIOR)

def evaluar_poblacion(poblacion):
    """Evalúa el fitness de cada individuo."""
    return [f(ind) for ind in poblacion]

def seleccionar_padres(poblacion, fitness):
    """Selecciona dos padres usando selección por torneo."""
    torneo = random.sample(list(zip(poblacion, fitness)), 3)
    torneo.sort(key=lambda x: x[1], reverse=True)
    return torneo[0][0], torneo[1][0]

def cruzar(padre1, padre2):
    """Cruza (promedio) entre dos padres."""
    alfa = random.random()
    hijo = alfa * padre1 + (1 - alfa) * padre2
    return hijo

def mutar(individuo):
    """Aplica una pequeña mutación aleatoria."""
    if random.random() < PROB_MUTACION:
        individuo += random.uniform(-1, 1)
    # Aseguramos que se mantenga dentro del rango permitido
    return max(min(individuo, LIM_SUPERIOR), LIM_INFERIOR)


# ----------------------------
# Algoritmo Genético principal
# ----------------------------
def algoritmo_genetico():
    # 1️⃣ Inicializar población
    poblacion = [generar_individuo() for _ in range(TAM_POBLACION)]

    mejor_global = None
    mejor_valor_global = float("-inf")

    for gen in range(GENERACIONES):
        # 2️⃣ Evaluar población
        fitness = evaluar_poblacion(poblacion)

        # Guardar mejor individuo global
        mejor_local = max(zip(poblacion, fitness), key=lambda x: x[1])
        if mejor_local[1] > mejor_valor_global:
            mejor_global, mejor_valor_global = mejor_local

        # 3️⃣ Nueva generación
        nueva_poblacion = []

        while len(nueva_poblacion) < TAM_POBLACION:
            # 4️⃣ Selección de padres
            p1, p2 = seleccionar_padres(poblacion, fitness)

            # 5️⃣ Cruza
            hijo = cruzar(p1, p2)

            # 6️⃣ Mutación
            hijo = mutar(hijo)

            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

        print(f"Generación {gen+1}: Mejor = {mejor_global:.4f}  f(x) = {mejor_valor_global:.4f}")

    return mejor_global, mejor_valor_global


# ----------------------------
# Ejemplo de uso
# ----------------------------
if __name__ == "__main__":
    random.seed(0)
    mejor_x, mejor_f = algoritmo_genetico()
    print("\n Mejor solución encontrada:")
    print(f"x = {mejor_x:.4f}, f(x) = {mejor_f:.4f}")
