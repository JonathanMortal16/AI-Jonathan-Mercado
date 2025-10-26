T = [
    [0.8, 0.4],  # Probabilidades de estar Soleado mañana
    [0.2, 0.6]   # Probabilidades de estar Lluvioso mañana
]

# Aquí asumimos que al inicio estamos 100% seguros que está Soleado.
P_actual = [1.0, 0.0]

def paso_markov(T, P):

    #Calcula la nueva distribución de probabilidad P_nueva = T * P
    soleado_mañana  = T[0][0] * P[0] + T[0][1] * P[1]
    lluvioso_mañana = T[1][0] * P[0] + T[1][1] * P[1]

    return [soleado_mañana, lluvioso_mañana]


print("Día\tProb(Soleado)\tProb(Lluvioso)")
print(f"0\t{P_actual[0]:.4f}\t\t{P_actual[1]:.4f}")

# Simulamos varios días aplicando SIEMPRE la MISMA matriz T
# Eso es lo que lo hace 'estacionario'
num_dias = 15

for dia in range(1, num_dias + 1):
    P_actual = paso_markov(T, P_actual)
    print(f"{dia}\t{P_actual[0]:.4f}\t\t{P_actual[1]:.4f}")
