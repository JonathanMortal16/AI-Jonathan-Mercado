# ============================================================
# Mapas Autoorganizados de Kohonen (SOM) - Versión Didáctica
# ============================================================

import numpy as np

class SOM:
    def __init__(self, grid_rows, grid_cols, input_dim, learning_rate=0.5, radius=None):
        """
        grid_rows, grid_cols: tamaño del mapa (rejilla)
        input_dim: dimensión de los vectores de entrada (por ejemplo 2, 3, 4, etc.)
        learning_rate: tasa de aprendizaje inicial
        radius: radio inicial de vecindad. Si no se da, usamos el máximo posible.
        """
        self.rows = grid_rows
        self.cols = grid_cols
        self.dim = input_dim
        self.lr0 = learning_rate

        # Inicializamos cada neurona con pesos aleatorios entre 0 y 1
        self.weights = np.random.rand(grid_rows, grid_cols, input_dim)

        # Radio inicial (vecindad). Ej: en un mapa 5x5 el radio máximo ~2.5
        if radius is None:
            self.radius0 = max(grid_rows, grid_cols) / 2
        else:
            self.radius0 = radius

    def _bmu(self, x):
        """
        Encuentra la BMU (Best Matching Unit)
        x: vector de entrada (shape: (input_dim,))
        Regresa: posición (i,j) de la neurona más cercana a x
        """
        # Calculamos distancia euclidiana de x a cada neurona
        diff = self.weights - x  # se broadcast a todo el mapa
        dist_sq = np.sum(diff**2, axis=2)  # distancia cuadrática en cada neurona
        bmu_index = np.unravel_index(np.argmin(dist_sq), (self.rows, self.cols))
        return bmu_index  # (i,j)

    def train(self, data, num_epochs=1000):
        """
        Entrenamos el SOM
        data: lista o array de vectores de entrenamiento
        num_epochs: cuántas iteraciones totales (epochs globales simplificados)
        """
        time_constant = num_epochs / np.log(self.radius0 + 1e-8)

        for t in range(num_epochs):
            # Elegimos un dato aleatorio
            x = data[np.random.randint(0, len(data))]

            # 1. Encontrar la BMU
            bmu_i, bmu_j = self._bmu(x)

            # 2. Calcular la tasa de aprendizaje y el radio de vecindad que van decayendo
            lr_t = self.lr0 * np.exp(-t / num_epochs)
            radius_t = self.radius0 * np.exp(-t / time_constant)

            # 3. Actualizar BMU y vecindad
            for i in range(self.rows):
                for j in range(self.cols):
                    # Distancia en la rejilla entre la neurona (i,j) y la BMU
                    dist_grid_sq = (i - bmu_i)**2 + (j - bmu_j)**2
                    if dist_grid_sq <= (radius_t**2):
                        # Influencia gaussiana: neuronas más cercanas cambian más
                        influence = np.exp(-dist_grid_sq / (2 * (radius_t**2) + 1e-8))
                        # Mover pesos hacia x
                        self.weights[i, j, :] += lr_t * influence * (x - self.weights[i, j, :])

            # (Opcional) cada cierto tiempo mostramos progreso
            if (t+1) % (num_epochs//5) == 0:
                print(f"Iteración {t+1}/{num_epochs} completada...")

    def map_point(self, x):
        """
        Devuelve la coordenada (fila, col) en el mapa donde cae el punto x
        (básicamente su BMU final).
        """
        return self._bmu(x)

# ============================================================
# DEMO DE USO
# ============================================================

if __name__ == "__main__":
    # Creamos un dataset sencillo de 3 "grupos" en 2D,
    # por ejemplo puntos alrededor de (0,0), (0,5), (5,0)
    cluster1 = np.random.normal(loc=[0.0, 0.0], scale=0.5, size=(50, 2))
    cluster2 = np.random.normal(loc=[0.0, 5.0], scale=0.5, size=(50, 2))
    cluster3 = np.random.normal(loc=[5.0, 0.0], scale=0.5, size=(50, 2))

    data = np.vstack([cluster1, cluster2, cluster3])

    # Creamos un SOM de 5x5 para datos 2D
    som = SOM(grid_rows=5, grid_cols=5, input_dim=2, learning_rate=0.5)

    # Entrenamos
    som.train(data, num_epochs=2000)

    # Probamos dónde cae cada centroide típico:
    test_points = np.array([
        [0.0, 0.0],
        [0.0, 5.0],
        [5.0, 0.0],
        [2.5, 2.5]
    ])

    print("\nUbicaciones en el mapa (BMU) de algunos puntos de prueba:")
    for p in test_points:
        pos = som.map_point(p)
        print(f"Punto {p} -> neurona {pos}")
