import random

# ================================
# 1. Definición de la gramática lexicalizada
# ================================
grammar = {
    "S": [
        (["NP", "VP"], "head_VP", 1.0)
    ],
    "NP": [
        (["Det", "N"], "head_N", 1.0)
    ],
    "VP": [
        (["V", "NP"], "head_V", 0.7),
        (["V"], "head_V", 0.3)
    ],
    # Terminales con sus "heads" (la palabra en sí misma)
    "Det": [
        (["el"], "el", 0.5),
        (["la"], "la", 0.5)
    ],
    "N": [
        (["gato"], "gato", 0.6),
        (["niña"], "niña", 0.4)
    ],
    "V": [
        (["ve"], "ve", 0.7),
        (["acaricia"], "acaricia", 0.3)
    ]
}

# ================================
# 2. Generador recursivo
# ================================
def generar(simbolo="S"):
    """Genera una oración y su probabilidad, manteniendo el head."""
    if simbolo not in grammar:
        # Es una palabra terminal
        return [simbolo], simbolo, 1.0

    reglas = grammar[simbolo]
    r = random.random()
    acum = 0.0
    for produccion, head_rule, p in reglas:
        acum += p
        if r <= acum:
            oracion = []
            prob_total = p
            heads = []
            for s in produccion:
                sub_oracion, sub_head, p_sub = generar(s)
                oracion.extend(sub_oracion)
                prob_total *= p_sub
                heads.append(sub_head)
            
            # Determinar head real
            if head_rule == "head_N":
                head = heads[-1]  # el sustantivo
            elif head_rule == "head_V":
                head = heads[0]   # el verbo
            elif head_rule == "head_VP":
                head = heads[-1]  # head del VP
            else:
                head = "?"        # por si acaso
            
            return oracion, head, prob_total
    return [], "?", 0.0

# ================================
# 3. Generar ejemplos
# ================================
print("=== Oraciones generadas con sus heads ===")
for i in range(5):
    oracion, head, p = generar()
    print(f"{i+1}. {' '.join(oracion)}   (head={head}, P={p:.4f})")
