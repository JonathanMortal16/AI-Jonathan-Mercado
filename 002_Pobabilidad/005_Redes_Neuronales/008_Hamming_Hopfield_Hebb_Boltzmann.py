
import numpy as np

# ------------------------------------------------------------
# Utilidades generales
# ------------------------------------------------------------

def sign_no_zero(x):
    """
    Función signo modificada:
    si x >= 0 -> +1
    si x < 0  -> -1
    Esto evita quedarnos en 0.
    """
    return 1 if x >= 0 else -1

def vector_sign(v):
    """
    Aplica sign_no_zero a cada elemento del vector v.
    """
    return np.array([sign_no_zero(x) for x in v])


# ------------------------------------------------------------
# (1) Regla de Hebb / Entrenamiento Hopfield
# ------------------------------------------------------------

class HopfieldNetwork:
    def __init__(self, num_neurons: int):
        # Matriz de pesos sinapsis N x N
        self.W = np.zeros((num_neurons, num_neurons))

    def train_hebb(self, patterns):
        """
        Entrenar con la regla hebbiana clásica:
        W = sum(p * p^T) para cada patrón p
        Luego se fuerza W_ii = 0 (sin auto-conexión)
        y se puede normalizar por número de patrones.
        """
        n = self.W.shape[0]
        self.W = np.zeros((n, n))  # reiniciamos por claridad

        for p in patterns:
            p = np.array(p)
            p = p.reshape(n, 1)  # columna
            self.W += p @ p.T    # outer product (Hebb)

        # Quitamos auto-conexiones
        np.fill_diagonal(self.W, 0)

        # Normalización opcional:
        self.W = self.W / len(patterns)

    def recall(self, input_pattern, steps=5):
        """
        Dado un patrón posiblemente ruidoso,
        lo iteramos varias veces hasta que converja
        a un patrón almacenado estable.
        """
        s = np.array(input_pattern, dtype=float)

        for _ in range(steps):
            # Actualización SINCRÓNICA (todas las neuronas a la vez)
            s = vector_sign(self.W @ s)

        return s

    def energy(self, state):
        """
        Energía de Hopfield / Boltzmann-like:
        E = -1/2 * s^T W s
        (mientras más baja, más estable el estado)
        """
        s = np.array(state)
        return -0.5 * s.T @ self.W @ s


# ------------------------------------------------------------
# (2) Clasificación tipo Hamming
# ------------------------------------------------------------

def hamming_distance(p1, p2):
    """
    Distancia de Hamming para vectores +/-1:
    Cuenta en cuántas posiciones difieren.
    """
    p1 = np.array(p1)
    p2 = np.array(p2)
    diffs = np.sum(p1 != p2)
    return diffs

def classify_by_similarity(test_pattern, stored_patterns):
    """
    Selecciona el patrón almacenado más parecido al test_pattern,
    usando distancia de Hamming mínima.
    Regresa:
      - índice del patrón más cercano
      - ese patrón
      - distancia
    """
    best_idx = None
    best_dist = None
    for i, pat in enumerate(stored_patterns):
        d = hamming_distance(test_pattern, pat)
        if best_dist is None or d < best_dist:
            best_dist = d
            best_idx = i
    return best_idx, stored_patterns[best_idx], best_dist


# ------------------------------------------------------------
# (3) DEMO INTEGRADA
# ------------------------------------------------------------
if __name__ == "__main__":
    # ========================================================
    # Definimos los "recuerdos" que queremos almacenar
    # Cada patrón es una lista de +1 / -1
    # Ejemplo con 6 neuronas
    # ========================================================
    patterns = [
        [+1, -1, +1, -1, +1, -1],  # Patrón A
        [+1, +1, -1, -1, +1, +1],  # Patrón B
        [-1, -1, +1, +1, -1, -1],  # Patrón C
    ]

    # Creamos la red Hopfield con tantas neuronas como bits por patrón
    num_neurons = len(patterns[0])
    net = HopfieldNetwork(num_neurons)

    # Entrenamos usando la regla de Hebb
    net.train_hebb(patterns)

    print("==== MATRIZ DE PESOS (W) ENTRENADA (regla de Hebb / Hopfield) ====")
    print(net.W)
    print()

    # ========================================================
    # Creamos una versión ruidosa de uno de los patrones
    # Por ejemplo tomamos el Patrón B pero le metemos errores
    # Patrón B original: [+1, +1, -1, -1, +1, +1]
    # Ruido: cambiamos 2 signos
    # ========================================================

    noisy = [+1, -1, -1, -1, +1, +1]  # parecido al B pero un bit cambió en la 2da posición
    print("Patrón ruidoso de entrada:")
    print(noisy)
    print()

    # ========================================================
    # Recuperación tipo Hopfield:
    # La red intenta "arreglar" el patrón ruidoso
    # ========================================================
    recovered = net.recall(noisy, steps=5)

    print("Patrón recuperado por la red (atracción Hopfield):")
    print(recovered.tolist())
    print()

    # ========================================================
    # Clasificación tipo Hamming:
    # ¿Este patrón recuperado a cuál patrón almacenado se parece más?
    # ========================================================
    idx, closest, dist = classify_by_similarity(recovered, patterns)
    print("El patrón recuperado se parece más al patrón almacenado #", idx)
    print("Patrón más cercano:", closest)
    print("Distancia de Hamming:", dist)
    print()

    # ========================================================
    # Energía del estado final:
    # Entre más baja la energía, más estable es el recuerdo.
    # (idea compartida entre Hopfield y Máquinas de Boltzmann:
    #  el sistema busca estados de baja energía)
    # ========================================================
    E = net.energy(recovered)
    print("Energía del estado final:", float(E))
    print()

    # Bonus: energía de cada uno de los patrones originales
    print("Energía de cada patrón original memorizado:")
    for i, p in enumerate(patterns):
        print(f" Patrón {i} {p} -> E = {float(net.energy(p))}")
