import random
from collections import defaultdict

# =========================
# 1. Corpus de entrenamiento
#    (puedes cambiar estas frases por apuntes, chats, etc.)
# =========================
corpus_frases = [
    "te quiero mucho",
    "te quiero demasiado",
    "te amo mucho",
    "yo te quiero",
    "yo te amo"
]

# =========================
# 2. Preprocesamiento
#    - pasamos a minúsculas
#    - agregamos tokens <INI> y <FIN>
# =========================
def preparar_corpus(frases):
    corpus_tokenizado = []
    for frase in frases:
        frase = frase.lower().strip()
        palabras = frase.split()
        # Agregamos marcadores de inicio y fin
        tokens = ["<INI>"] + palabras + ["<FIN>"]
        corpus_tokenizado.append(tokens)
    return corpus_tokenizado

corpus_tokens = preparar_corpus(corpus_frases)

# =========================
# 3. Contar frecuencias de bigramas
#    bigramas[(w1, w2)] = cuántas veces vimos w1 seguido de w2
#    conteo_unigramas[w1] = cuántas veces vimos w1 como "palabra previa"
# =========================
bigramas = defaultdict(int)
conteo_unigramas = defaultdict(int)

for tokens in corpus_tokens:
    for i in range(len(tokens) - 1):
        w1 = tokens[i]
        w2 = tokens[i+1]
        bigramas[(w1, w2)] += 1
        conteo_unigramas[w1] += 1

# =========================
# 4. Función para obtener P(siguiente | actual)
#    P(w2 | w1) = conteo(w1,w2) / conteo(w1)
# =========================
def prob_condicional(w1, w2):
    num = bigramas[(w1, w2)]
    den = conteo_unigramas[w1]
    if den == 0:
        return 0.0
    return num / den

# =========================
# 5. Mostrar tabla de probabilidades aprendidas
# =========================
print("=== Probabilidades condicionales aprendidas (P(siguiente | actual)) ===")
vistos = set()
for (w1, w2), cnt in bigramas.items():
    if (w1, w2) in vistos:
        continue
    vistos.add((w1, w2))
    p = prob_condicional(w1, w2)
    print(f"P({w2!r} | {w1!r}) = {p:.3f}")

# =========================
# 6. Calcular la probabilidad aproximada de una oración
#    usando el modelo de bigramas
# =========================
def prob_oracion(oracion_palabras):
    """
    oracion_palabras: lista de palabras sin <INI>/<FIN>
    ejemplo: ["te", "quiero", "mucho"]
    """
    tokens = ["<INI>"] + oracion_palabras + ["<FIN>"]
    p_total = 1.0
    for i in range(len(tokens) - 1):
        w1 = tokens[i]
        w2 = tokens[i+1]
        p = prob_condicional(w1, w2)
        # Si nunca vimos ese bigrama en el corpus, p = 0
        p_total *= p
    return p_total

ejemplo = ["te", "quiero", "mucho"]
print("\n=== Probabilidad aproximada de la oración:", " ".join(ejemplo), "===")
print("P =", prob_oracion(ejemplo))

# =========================
# 7. Generar texto aleatorio según el modelo
#    Empieza en <INI> y elige la siguiente palabra
#    de acuerdo a las probabilidades P(w2|w1)
# =========================
def generar_frase(max_palabras=10):
    palabra_actual = "<INI>"
    frase_generada = []
    
    for _ in range(max_palabras):
        # Reunir todas las palabras posibles después de palabra_actual
        candidatos = []
        probs = []
        total_local = 0
        
        for (w1, w2), cnt in bigramas.items():
            if w1 == palabra_actual:
                candidatos.append(w2)
                p = prob_condicional(w1, w2)
                probs.append(p)
                total_local += p
        
        if not candidatos:
            # No sabemos continuar
            break
        
        # Normalizar (por si hay redondeos)
        # Creamos una ruleta proporcional a probs
        r = random.random()
        acum = 0.0
        elegido = candidatos[-1]  # fallback
        
        for cand, p in zip(candidatos, probs):
            acum += p
            if r <= acum:
                elegido = cand
                break
        
        if elegido == "<FIN>":
            break
        
        frase_generada.append(elegido)
        palabra_actual = elegido
    
    return " ".join(frase_generada)

print("\n=== Frases generadas por el modelo ===")
for _ in range(5):
    print("-", generar_frase())
