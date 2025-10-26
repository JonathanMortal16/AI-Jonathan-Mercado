# Distribución de probabilidad del clima
distribucion_clima = {
    "Soleado": 0.5,
    "Nublado": 0.3,
    "Lluvioso": 0.2
}

# Mostrar distribución
print("Distribución de probabilidad del clima:")
for estado, prob in distribucion_clima.items():
    print(f"{estado}: {prob}")

# Comprobación: las probabilidades deben sumar 1
suma = sum(distribucion_clima.values())
print("\nSuma total =", suma)

# Normalización (por si no suman exactamente 1)
if abs(suma - 1.0) > 0.001:
    print("La distribución no está normalizada. Normalizando...")
    distribucion_clima = {k: v / suma for k, v in distribucion_clima.items()}
    print("\nDistribución normalizada:")
    for estado, prob in distribucion_clima.items():
        print(f"{estado}: {round(prob, 3)}")

