from collections import defaultdict, Counter

# ============================================
# 1. Corpus paralelo (español -> inglés)
#    Seguimos el mismo principio, pero lo usaremos 2 veces:
#    (a) para aprender traducciones palabra->palabra
#    (b) para extraer también frases comunes (n-gramas)
# ============================================
corpus_paralelo = [
    ("yo te quiero",             "i love you"),
    ("te amo mucho",             "i love you very much"),
    ("te quiero mucho",          "i love you very much"),
    ("buenas noches",            "good night"),
    ("buenos dias",              "good morning"),
    ("gracias",                  "thank you"),
    ("hola",                     "hello"),
    ("como estas",               "how are you"),
    ("estoy bien",               "i am fine"),
    ("te amo",                   "i love you")
]

# ============================================
# 2. Extraer diccionario de frases directas
#    Guardamos equivalencias multi-palabra exactas
#    Esto simula phrase-based SMT.
# ============================================
frase_dict = {}
for es, en in corpus_paralelo:
    frase_dict[es] = en

# ============================================
# 3. Aprender traducción palabra->palabra (IBM1-ish)
#    Contamos co-ocurrencias: cada palabra ES con cada palabra EN
# ============================================
coocurrencias = defaultdict(Counter)
for es_sentence, en_sentence in corpus_paralelo:
    es_words = es_sentence.lower().split()
    en_words = en_sentence.lower().split()
    for w_es in es_words:
        for w_en in en_words:
            coocurrencias[w_es][w_en] += 1

tabla_traduccion = defaultdict(dict)
for w_es, counter_en in coocurrencias.items():
    total = sum(counter_en.values())
    for w_en, cnt in counter_en.items():
        tabla_traduccion[w_es][w_en] = cnt / total

def mejores_traducciones(w_es):
    if w_es not in tabla_traduccion:
        return []
    cand = list(tabla_traduccion[w_es].items())
    cand.sort(key=lambda x: x[1], reverse=True)
    return cand

# ============================================
# 4. Priorizador de traducciones empatadas
#    (mini modelo de lenguaje destino "hardcoded")
# ============================================
preferencias_en = {
    # pronombres
    "yo":    ["i", "me"],
    "te":    ["you"],
    # verbos afectar/cariño
    "amo":   ["love", "like", "adore", "i"],
    "quiero":["love", "want", "i"],
    # saludos
    "buenas":["good"],
    "buenos":["good"],
    "dias":  ["morning"],
    "noches":["night"],
    # estructura de saludo/pregunta
    "como":  ["how"],
    "estas": ["are", "you"],
    "estoy": ["i", "am"],
    "bien":  ["fine", "good"],
    "gracias":["thank", "thanks", "thank you"],
    "mucho": ["very", "much"]
}

def elegir_mejor_traduccion_palabra(w_es):
    # si no tenemos info, devolvemos la palabra en corchetes
    if w_es not in tabla_traduccion:
        return "[" + w_es + "]"
    cand = mejores_traducciones(w_es)

    # cand es lista de (palabra_en, prob)
    # intentamos alinear con preferencias_en
    if w_es in preferencias_en:
        prefs = preferencias_en[w_es]
        for pref in prefs:
            for palabra_en, _p in cand:
                if palabra_en == pref:
                    return palabra_en

    # si no hay preferencia que cuadre, tomamos el top por prob
    return cand[0][0]

# ============================================
# 5. Traducción con frases primero
#    - Intentamos cubrir la oración con la frase más larga conocida.
#    - Si no hay frase exacta, caemos palabra a palabra.
# ============================================
def traducir_es_a_en(oracion_es):
    oracion_es = oracion_es.lower().strip()
    palabras = oracion_es.split()

    # estrategia greedy: checar primero si hay match de frases largas
    # probamos n-gramas desde tamaño grande a chico
    resultado_en = []
    i = 0
    while i < len(palabras):
        match_encontrado = False
        
        # intentamos window size de 4,3,2 palabras (puedes ajustar)
        for window in [4,3,2]:
            if i + window <= len(palabras):
                segmento = " ".join(palabras[i:i+window])
                if segmento in frase_dict:
                    # usamos traducción directa de la frase
                    resultado_en.append(frase_dict[segmento])
                    i += window
                    match_encontrado = True
                    break
        
        if match_encontrado:
            continue

        # si no hubo frase multi-palabra, traducimos palabra individual
        w_es = palabras[i]
        w_en = elegir_mejor_traduccion_palabra(w_es)
        resultado_en.append(w_en)
        i += 1

    # Unimos resultados parciales.
    # Nota: como agregamos frases completas ("i love you") como bloques,
    # aquí solo join con espacio. Luego podemos limpiar espacios dobles.
    traduccion = " ".join(resultado_en)
    # limpieza rápida: "thank you" en lugar de "thank you" como dos bloques separados
    traduccion = traduccion.replace("  ", " ").strip()
    return traduccion

# ============================================
# 6. Demo
# ============================================
print("=== Tabla de traducción aprendida (top candidatos) ===")
for w_es in sorted(tabla_traduccion.keys()):
    print(f"{w_es:12s} -> {mejores_traducciones(w_es)[:3]}")
print()

tests = [
    "yo te amo mucho",
    "te quiero mucho",
    "buenas noches",
    "buenos dias",
    "como estas",
    "gracias",
    "estoy bien"
]

print("=== Traducciones generadas mejoradas ===")
for t in tests:
    print(f"{t:20s} -> {traducir_es_a_en(t)}")
