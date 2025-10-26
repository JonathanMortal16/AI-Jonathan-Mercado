# =============================================
# PERCEPTRÓN: Clasificador binario (AND)
# =============================================

import random

class Perceptron:
    def __init__(self, num_inputs, lr=0.1):
        self.weights = [random.uniform(-1, 1) for _ in range(num_inputs)]
        self.bias = random.uniform(-1, 1)
        self.lr = lr

    def activation(self, x):
        """Función de activación escalón"""
        return 1 if x >= 0 else 0

    def predict(self, inputs):
        total = sum(w*x for w, x in zip(self.weights, inputs)) + self.bias
        return self.activation(total)

    def train(self, training_data, epochs=10):
        for epoch in range(epochs):
            total_error = 0
            for inputs, expected in training_data:
                prediction = self.predict(inputs)
                error = expected - prediction
                total_error += abs(error)
                # Ajuste de pesos y bias
                self.weights = [w + self.lr * error * x for w, x in zip(self.weights, inputs)]
                self.bias += self.lr * error
            print(f"Epoch {epoch+1}: Error total = {total_error}")

# Dataset para AND lógico
training_data = [
    ([0, 0], 0),
    ([0, 1], 0),
    ([1, 0], 0),
    ([1, 1], 1)
]

p = Perceptron(num_inputs=2)
p.train(training_data, epochs=10)

print("\nPruebas:")
for x in training_data:
    print(f"{x[0]} -> {p.predict(x[0])}")
