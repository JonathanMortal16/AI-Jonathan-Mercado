import random
import math
def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# -----------------------------
# Generar datos de ejemplo (sin etiquetas)
# -----------------------------
random.seed(0)
datos = []

# Grupo 1 (cerca de (2, 2))
for _ in range(10):
    datos.append((random.uniform(1.5, 2.5), random.uniform(1.5, 2.5)))

# Grupo 2 (cerca de (7, 7))
for _ in range(10):
    datos.append((random.uniform(6.5, 7.5), random.uniform(6.5, 7.5)))

# Grupo 3 (cerca de (3, 8))
for _ in range(10):
    datos.append((random.uniform(2.5, 3.5), random.uniform(7.5, 8.5)))

# -----------------------------
# Parámetros iniciales
# -----------------------------
k = 3  # número de grupos
max_iter = 10  # número máximo de iteraciones

# Inicializar centroides aleatoriamente de entre los datos
centroides = random.sample(datos, k)

print("Centroides iniciales:")
for i, c in enumerate(centroides):
    print(f"  C{i+1} = {c}")
print()

# -----------------------------
# Algoritmo principal
# -----------------------------
for iteracion in range(1, max_iter + 1):

    # Paso 1: Asignar cada punto al centro más cercano
    grupos = [[] for _ in range(k)]

    for punto in datos:
        distancias = [distancia(punto, c) for c in centroides]
        indice_min = distancias.index(min(distancias))
        grupos[indice_min].append(punto)

    # Paso 2: Recalcular cada centro como promedio del grupo
    nuevos_centroides = []
    for grupo in grupos:
        if len(grupo) > 0:
            x_prom = sum(p[0] for p in grupo) / len(grupo)
            y_prom = sum(p[1] for p in grupo) / len(grupo)
            nuevos_centroides.append((x_prom, y_prom))
        else:
            # si un grupo quedó vacío, mantenemos el centro viejo
            nuevos_centroides.append(random.choice(datos))

    # Imprimir progreso
    print(f"Iteración {iteracion}:")
    for i, c in enumerate(nuevos_centroides):
        print(f"  Centro {i+1} = {c}")
    print()

    # Revisar si los centros dejaron de cambiar
    if nuevos_centroides == centroides:
        print("Convergencia alcanzada.")
        break

    centroides = nuevos_centroides

# -----------------------------
# Mostrar resultado final
# -----------------------------
print("=== Resultados Finales ===")
for i, grupo in enumerate(grupos):
    print(f"Grupo {i+1} ({len(grupo)} puntos):")
    for p in grupo:
        print(f"  {p}")
    print(f"Centro final: {centroides[i]}")
    print()
