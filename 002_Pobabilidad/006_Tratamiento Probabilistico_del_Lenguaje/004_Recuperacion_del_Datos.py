from collections import Counter
import math

# ===============================
# 1. Corpus de documentos
# ===============================
docs = {
    "D1": "gato negro duerme",
    "D2": "perro marrón corre",
    "D3": "gato come pescado"
}

# ===============================
# 2. Función: construir modelo de lenguaje para cada documento
# ===============================
def construir_modelo(doc_texto):
    palabras = doc_texto.lower().split()
    total = len(palabras)
    conteos = Counter(palabras)
    vocab = set(conteos.keys())
    return conteos, total, vocab

# Crear modelos
modelos = {}
vocab_total = set()
for nombre, texto in docs.items():
    conteos, total, vocab = construir_modelo(texto)
    modelos[nombre] = (conteos, total)
    vocab_total |= vocab

# ===============================
# 3. Calcular P(Q|D)
#    Usando suavizado de Laplace
# ===============================
def prob_consulta_dado_doc(consulta, conteos, total, vocab):
    palabras_q = consulta.lower().split()
    V = len(vocab)
    log_prob = 0.0
    for palabra in palabras_q:
        freq = conteos.get(palabra, 0)
        # suavizado laplace: (freq + 1) / (total + V)
        p = (freq + 1) / (total + V)
        log_prob += math.log(p)
    return math.exp(log_prob)  # devuelvo probabilidad

# ===============================
# 4. Consulta
# ===============================
consulta = "gato duerme"
print("Consulta:", consulta, "\n")

ranking = []
for nombre, (conteos, total) in modelos.items():
    p_q_d = prob_consulta_dado_doc(consulta, conteos, total, vocab_total)
    ranking.append((nombre, p_q_d))

# ===============================
# 5. Mostrar resultados ordenados
# ===============================
ranking.sort(key=lambda x: x[1], reverse=True)
print("=== Resultados ordenados por probabilidad P(Q|D) ===")
for doc, prob in ranking:
    print(f"{doc}: {prob:.6f}")
