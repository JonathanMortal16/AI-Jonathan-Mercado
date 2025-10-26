import random

# Definimos los estados posibles
estados = ["Soleado", "Lluvioso"]

# Matriz de transición (constante en el tiempo)
# T[nuevo][actual] = Prob( ir a 'nuevo' dado 'actual' )
T = [
    [0.8, 0.4],  # Prob de estar Soleado mañana
    [0.2, 0.6]   # Prob de estar Lluvioso mañana
]

# Estado inicial (día 0)
estado_actual = 0  # 0 = Soleado, 1 = Lluvioso

# Función para elegir el siguiente estado con base en las probabilidades
def siguiente_estado(estado_actual):
    prob = random.random()  # número aleatorio entre 0 y 1
    if prob < T[1][estado_actual]:  # Si cae en la prob. de Lluvioso
        return 1
    else:
        return 0

# Simulación de varios días
num_dias = 10
print("Día\tClima")
print(f"0\t{estados[estado_actual]}")

for dia in range(1, num_dias + 1):
    estado_actual = siguiente_estado(estado_actual)
    print(f"{dia}\t{estados[estado_actual]}")
