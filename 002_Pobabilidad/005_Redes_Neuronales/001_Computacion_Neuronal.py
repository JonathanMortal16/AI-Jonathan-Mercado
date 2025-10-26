import random

class Perceptron:
    def __init__(self, num_inputs, learning_rate=0.1):
        # Inicializamos pesos pequeños aleatorios
        self.weights = [random.uniform(-1, 1) for _ in range(num_inputs)]
        # Bias (sesgo), también aleatorio al inicio
        self.bias = random.uniform(-1, 1)
        # Tasa de aprendizaje: qué tan agresivo corrige los errores
        self.lr = learning_rate

    def activation(self, x):
        """
        Función de activación escalón:
        si la suma >= 0 -> 1
        si la suma < 0 -> 0
        Esta simula el "se dispara / no se dispara" de una neurona.
        """
        return 1 if x >= 0 else 0

    def predict(self, inputs):
        """
        Calcula la salida actual de la neurona:
        salida = activacion( w·x + bias )
        """
        # Producto punto w·x (peso * entrada y lo sumamos)
        total = 0
        for w, x in zip(self.weights, inputs):
            total += w * x

        # Sumamos el bias (desplaza la frontera de decisión)
        total += self.bias

        # Pasamos por la activación
        return self.activation(total)

    def train(self, training_data, epochs=20):
        """
        Entrenamiento tipo perceptrón:
        Recorremos los datos muchas veces (epochs),
        medimos el error, y ajustamos pesos y bias.
        """
        for epoch in range(epochs):
            total_error = 0

            for inputs, desired_output in training_data:
                prediction = self.predict(inputs)
                error = desired_output - prediction
                total_error += abs(error)

                # Regla de actualización de perceptrón:
                # w_i(new) = w_i(old) + lr * error * x_i
                # bias(new) = bias(old) + lr * error
                for i in range(len(self.weights)):
                    self.weights[i] += self.lr * error * inputs[i]
                self.bias += self.lr * error

            # Mostramos el progreso de entrenamiento
            print(f"Epoch {epoch+1} | Error total: {total_error}")
            print(f"  Pesos: {self.weights}")
            print(f"  Bias : {self.bias}")
            print("---------------------------")


# ============================
# 1) Creamos el dataset de la compuerta lógica AND
# ============================

training_data = [
    ([0, 0], 0),  # 0 AND 0 = 0
    ([0, 1], 0),  # 0 AND 1 = 0
    ([1, 0], 0),  # 1 AND 0 = 0
    ([1, 1], 1)   # 1 AND 1 = 1
]

# ============================
# 2) Creamos la neurona (2 entradas porque AND tiene 2 bits)
# ============================

perceptron = Perceptron(num_inputs=2, learning_rate=0.1)

# ============================
# 3) Entrenamos
# ============================
perceptron.train(training_data, epochs=20)

# ============================
# 4) Probamos la neurona ya entrenada
# ============================

print("\nProbando la neurona entrenada:")
tests = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]

for t in tests:
    print(f"Entrada {t} -> Salida de la neurona: {perceptron.predict(t)}")
