import random

# ================================
# 1. Definición de la PCFG
# ================================
# Cada no terminal tiene una lista de reglas con su probabilidad asociada.
grammar = {
    "S": [
        (["NP", "VP"], 1.0)
    ],
    "NP": [
        (["Det", "N"], 0.9),
        (["N"], 0.1)
    ],
    "VP": [
        (["V", "NP"], 0.6),
        (["V"], 0.4)
    ],
    "Det": [
        (["el"], 0.5),
        (["la"], 0.5)
    ],
    "N": [
        (["gato"], 0.6),
        (["niña"], 0.4)
    ],
    "V": [
        (["ve"], 0.7),
        (["acaricia"], 0.3)
    ]
}

# ================================
# 2. Generador recursivo de oraciones
# ================================
def generar(simbolo="S"):
    """Genera una oración aleatoria a partir de la gramática."""
    if simbolo not in grammar:
        # Es un terminal (palabra)
        return [simbolo], 1.0

    # Selecciona una regla de producción según sus probabilidades
    reglas = grammar[simbolo]
    r = random.random()
    acumulado = 0.0
    for produccion, prob in reglas:
        acumulado += prob
        if r <= acumulado:
            oracion = []
            prob_total = prob
            for s in produccion:
                sub_oracion, p_sub = generar(s)
                oracion.extend(sub_oracion)
                prob_total *= p_sub
            return oracion, prob_total

    # Si no entra (por redondeo)
    return [], 0.0

# ================================
# 3. Generar múltiples ejemplos
# ================================
print("=== Oraciones generadas por la PCFG ===")
for i in range(5):
    oracion, p = generar()
    print(f"{i+1}. {' '.join(oracion)}  (P={p:.4f})")
