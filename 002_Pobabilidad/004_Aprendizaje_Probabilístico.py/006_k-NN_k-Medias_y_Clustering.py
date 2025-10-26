import math
import random
from collections import Counter

# ============================================================
# k-NN, k-MEDIAS y CLUSTERING
# ============================================================

# ------------------------------------------------------------
# 1. k-NN (k-Nearest Neighbors)
# ------------------------------------------------------------

def distancia(p1, p2):
    """Distancia euclidiana entre dos puntos 2D."""
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def knn_clasificar(datos_entrenamiento, nuevo_punto, k=3):
    """
    datos_entrenamiento: lista de (x, y, etiqueta)
    nuevo_punto: (x, y)
    """
    # Calculamos distancia de cada punto al nuevo
    distancias = []
    for x, y, etiqueta in datos_entrenamiento:
        d = distancia((x, y), nuevo_punto)
        distancias.append((d, etiqueta))
    # Ordenar y tomar los k más cercanos
    distancias.sort(key=lambda x: x[0])
    vecinos = distancias[:k]
    # Contar las etiquetas más frecuentes
    etiquetas = [et for _, et in vecinos]
    etiqueta_pred = Counter(etiquetas).most_common(1)[0][0]
    return etiqueta_pred

# Dataset simple con etiquetas (supervisado)
datos_knn = [
    (1.0, 1.2, 'A'), (1.5, 1.8, 'A'), (2.0, 2.1, 'A'),
    (6.0, 6.5, 'B'), (6.5, 7.0, 'B'), (7.0, 6.8, 'B')
]

nuevo = (2.5, 2.3)
etiqueta_pred = knn_clasificar(datos_knn, nuevo, k=3)

print("=== k-NN ===")
print(f"Punto nuevo: {nuevo}")
print(f"Clase predicha: {etiqueta_pred}")
print()

# ------------------------------------------------------------
# 2. k-MEDIAS (k-Means) - no supervisado
# ------------------------------------------------------------

# Generar datos sin etiquetas
random.seed(0)
datos = []

# Grupo 1 (cerca de (2,2))
for _ in range(8):
    datos.append((random.uniform(1.5, 2.5), random.uniform(1.5, 2.5)))
# Grupo 2 (cerca de (7,7))
for _ in range(8):
    datos.append((random.uniform(6.5, 7.5), random.uniform(6.5, 7.5)))
# Grupo 3 (cerca de (3,8))
for _ in range(8):
    datos.append((random.uniform(2.5, 3.5), random.uniform(7.5, 8.5)))

# Inicializar centroides
k = 3
centroides = random.sample(datos, k)

# Ejecutar 5 iteraciones de k-medias
for iteracion in range(5):
    grupos = [[] for _ in range(k)]
    # Asignación
    for punto in datos:
        dist = [distancia(punto, c) for c in centroides]
        idx = dist.index(min(dist))
        grupos[idx].append(punto)
    # Recalcular centroides
    nuevos_centroides = []
    for grupo in grupos:
        if len(grupo) > 0:
            x_prom = sum(p[0] for p in grupo) / len(grupo)
            y_prom = sum(p[1] for p in grupo) / len(grupo)
            nuevos_centroides.append((x_prom, y_prom))
        else:
            nuevos_centroides.append(random.choice(datos))
    centroides = nuevos_centroides

print("=== k-MEDIAS ===")
for i, c in enumerate(centroides):
    print(f"Centro {i+1}: {c}")
print()

# ------------------------------------------------------------
# 3. Clustering general (explicación conceptual)
# ------------------------------------------------------------
print("=== CLUSTERING ===")
print("El agrupamiento no supervisado detecta patrones sin etiquetas.")
print("En este ejemplo, k-medias ha identificado grupos naturales de datos.")
print("Otros métodos de clustering: jerárquico, DBSCAN, mezcla gaussiana, etc.")
