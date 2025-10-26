import math

# --------------------------
# 1. Datos de entrenamiento
# --------------------------
# Cada elemento es (texto, etiqueta)
# etiqueta es "pos" (positivo) o "neg" (negativo)
dataset_entrenamiento = [
    ("me encanta este producto es excelente",    "pos"),
    ("es muy bueno me gusta demasiado",          "pos"),
    ("amo la calidad y el servicio",             "pos"),
    ("esto fue horrible no me gustó nada",       "neg"),
    ("muy malo estoy decepcionado",              "neg"),
    ("odio la experiencia fue terrible",         "neg"),
]

# ---------------------------------------
# 2. Función para partir texto en tokens
# ---------------------------------------
def tokenizar(frase):
    """
    Convierte una frase en una lista de palabras.
    Aquí lo hacemos súper simple:
    - pasamos todo a minúsculas
    - separamos por espacios
    No quitamos acentos ni puntuación fina, pero se podría.
    """
    return frase.lower().split()

# -------------------------------------------------------
# 3. ENTRENAMIENTO DEL MODELO NAÏVE BAYES
# -------------------------------------------------------
def entrenar_naive_bayes(dataset):
    """
    Devuelve un modelo con:
      - conteos de palabras por clase
      - total de palabras por clase
      - P(clase)
      - vocabulario total
    """

    # Contadores
    conteo_clase = {}             # cuántos documentos hay en cada clase
    conteo_palabra_en_clase = {}  # dict anidado: {clase: {palabra: conteo}}
    total_palabras_en_clase = {}  # total de palabras (con repeticiones) por clase
    vocabulario = set()           # conjunto de todas las palabras

    total_documentos = len(dataset)

    # Inicializamos estructuras
    for _, etiqueta in dataset:
        if etiqueta not in conteo_clase:
            conteo_clase[etiqueta] = 0
            conteo_palabra_en_clase[etiqueta] = {}
            total_palabras_en_clase[etiqueta] = 0

    # Recorremos cada ejemplo del dataset
    for texto, etiqueta in dataset:
        conteo_clase[etiqueta] += 1  # contamos documento en esa clase

        palabras = tokenizar(texto)
        for w in palabras:
            vocabulario.add(w)

            # sumamos 1 al conteo de esa palabra en esa clase
            if w not in conteo_palabra_en_clase[etiqueta]:
                conteo_palabra_en_clase[etiqueta][w] = 0
            conteo_palabra_en_clase[etiqueta][w] += 1

            # y aumentamos el total de palabras en esa clase
            total_palabras_en_clase[etiqueta] += 1

    # Calculamos P(clase) a partir de frecuencia relativa
    prob_clase = {}
    for etiqueta in conteo_clase:
        prob_clase[etiqueta] = conteo_clase[etiqueta] / total_documentos

    # Empaquetamos todo en un "modelo"
    modelo = {
        "prob_clase": prob_clase,
        "conteo_palabra_en_clase": conteo_palabra_en_clase,
        "total_palabras_en_clase": total_palabras_en_clase,
        "vocabulario": vocabulario,
        "tam_vocab": len(vocabulario)
    }

    return modelo

# -------------------------------------------------------
# 4. FUNCION PARA CALCULAR P(clase | texto nuevo)
#    usando log-probabilidades
# -------------------------------------------------------
def puntaje_log_prob_clase(modelo, texto, clase):
    """
    Calcula el "score" log(P(clase) * Π P(palabra|clase))
    = log P(clase) + sum(log P(palabra|clase))
    Usamos suavizado de Laplace: +1 en conteos.
    """

    prob_clase = modelo["prob_clase"][clase]
    conteo_palabra_en_clase = modelo["conteo_palabra_en_clase"][clase]
    total_palabras_clase = modelo["total_palabras_en_clase"][clase]
    tam_vocab = modelo["tam_vocab"]

    # empezamos con log P(clase)
    score = math.log(prob_clase)

    palabras = tokenizar(texto)

    for w in palabras:
        # conteo de esa palabra en la clase (0 si nunca apareció)
        conteo_w = conteo_palabra_en_clase.get(w, 0)

        # Probabilidad con suavizado de Laplace:
        # (conteo_w + 1) / (total_palabras_clase + tam_vocab)
        prob_w_dada_clase = (conteo_w + 1) / (total_palabras_clase + tam_vocab)

        # sumamos log(prob_w_dada_clase)
        score += math.log(prob_w_dada_clase)

    return score

# -------------------------------------------------------
# 5. PREDICCIÓN FINAL
# -------------------------------------------------------
def predecir(modelo, texto):
    """
    Calcula el score para cada clase y devuelve la mejor.
    También devuelve los scores para ver la confianza relativa.
    """
    scores = {}
    for clase in modelo["prob_clase"]:
        scores[clase] = puntaje_log_prob_clase(modelo, texto, clase)

    # Elegimos la clase con score log mayor (más probable)
    mejor_clase = max(scores, key=scores.get)
    return mejor_clase, scores


# ============================================================
# EJEMPLO DE USO
# ============================================================

# Entrenamos el modelo con el dataset de arriba
modelo = entrenar_naive_bayes(dataset_entrenamiento)

# Probemos algunas frases nuevas
frases_prueba = [
    "me encantó la calidad es muy bueno",
    "fue terrible y estoy muy decepcionado",
    "no me gustó pero el servicio fue bueno",
    "amo esto",
    "horrible experiencia la odio",
]

print("=== CLASIFICADOR NAÏVE BAYES (pos / neg) ===\n")

for frase in frases_prueba:
    etiqueta_predicha, scores = predecir(modelo, frase)

    print(f"Frase: \"{frase}\"")
    print(f" -> Clase predicha: {etiqueta_predicha}")
    print(f"    Score log(pos): {scores.get('pos', None)}")
    print(f"    Score log(neg): {scores.get('neg', None)}\n")
