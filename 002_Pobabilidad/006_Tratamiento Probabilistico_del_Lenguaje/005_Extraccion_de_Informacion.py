from collections import defaultdict, Counter
import math
import re

# =====================================
# 1. Corpus de entrenamiento con etiquetas (palabra, etiqueta)
#    Agregamos ejemplos para que conozca Steve Jobs y Apple.
# =====================================
# PER = Persona
# ORG = Organización
# LOC = Lugar
# O   = Otro
entrenamiento = [
    # Ejemplo 1
    ("Elon", "PER"), ("Musk", "PER"), ("fundó", "O"), ("SpaceX", "ORG"),
    ("en", "O"), ("2002", "O"), ("en", "O"), ("California", "LOC"),

    # Ejemplo 2
    ("Bill", "PER"), ("Gates", "PER"), ("fundó", "O"), ("Microsoft", "ORG"),
    ("en", "O"), ("1975", "O"), ("en", "O"), ("Albuquerque", "LOC"),

    # Ejemplo 3 (nuevo, para que el modelo "aprenda" antes de probar)
    ("Steve", "PER"), ("Jobs", "PER"), ("fundó", "O"), ("Apple", "ORG"),
    ("en", "O"), ("1976", "O"), ("en", "O"), ("California", "LOC"),
]

# =====================================
# 2. Calculamos P(etiqueta) y P(palabra | etiqueta)
# =====================================
freq_palabra_etiqueta = defaultdict(Counter)
freq_etiqueta = Counter()

for palabra, etiqueta in entrenamiento:
    freq_palabra_etiqueta[etiqueta][palabra] += 1
    freq_etiqueta[etiqueta] += 1

total_etiquetas = sum(freq_etiqueta.values())
vocabulario = set([p for p, _ in entrenamiento])

def prob_palabra_dado_etiqueta(palabra, etiqueta):
    """
    Probabilidad con suavizado de Laplace:
    P(palabra|etiqueta) = (conteo(palabra,etiqueta)+1) / (conteo_total_etiqueta + |V|)
    """
    freq = freq_palabra_etiqueta[etiqueta][palabra]
    total = sum(freq_palabra_etiqueta[etiqueta].values())
    V = len(vocabulario)
    return (freq + 1) / (total + V)

def prob_etiqueta(etiqueta):
    """
    Prior de la etiqueta: P(etiqueta)
    """
    return freq_etiqueta[etiqueta] / total_etiquetas

# =====================================
# 3. Heurísticas suaves (ayudan cuando la palabra es desconocida)
# =====================================
def bonus_heuristico(palabra, etiqueta, posicion):
    """
    Devuelve un multiplicador (>1 favorece esa etiqueta)
    Basado en pistas superficiales del idioma.
    """
    # Si es un año de 4 dígitos tipo 1976, 2002 -> probablemente "O"
    if re.fullmatch(r"\d{4}", palabra):
        if etiqueta == "O":
            return 1.5
        else:
            return 0.5

    # Si empieza en mayúscula y no es la primera palabra,
    # suele ser Nombre Propio (persona u organización o lugar).
    if palabra[0].isupper() and posicion > 0:
        if etiqueta in ("PER", "ORG", "LOC"):
            return 1.3
        else:
            return 0.7

    # Default: sin cambio
    return 1.0

# =====================================
# 4. Clasificador de una palabra
# =====================================
def etiqueta_mas_probable(palabra, posicion):
    """
    Estima la mejor etiqueta para 'palabra' usando:
    - Naïve Bayes palabra→etiqueta
    - Priors de etiqueta
    - Heurística extra
    Regresa la mejor etiqueta y el puntaje por etiqueta.
    """
    puntajes = {}
    for etiqueta in freq_etiqueta.keys():
        # P(etiqueta) * P(palabra|etiqueta)
        base = prob_etiqueta(etiqueta) * prob_palabra_dado_etiqueta(palabra, etiqueta)
        # Ajuste heurístico
        ajustado = base * bonus_heuristico(palabra, etiqueta, posicion)
        puntajes[etiqueta] = ajustado

    mejor = max(puntajes, key=puntajes.get)
    return mejor, puntajes

# =====================================
# 5. Probar con texto NUEVO
# =====================================
texto = "Steve Jobs fundó Apple en 1976 en California"
palabras = texto.split()

print("=== Extracción de Información Probabilística (Mejorada) ===")
for i, palabra in enumerate(palabras):
    etiqueta, puntajes = etiqueta_mas_probable(palabra, i)
    print(f"{palabra:12s} -> {etiqueta}")
