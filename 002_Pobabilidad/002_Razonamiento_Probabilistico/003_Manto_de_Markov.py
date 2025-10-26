# Definimos las relaciones de padres e hijos en la red
red_bayesiana = {
    "A": {"padres": [],        "hijos": ["B", "C"]},
    "B": {"padres": ["A"],     "hijos": ["D"]},
    "C": {"padres": ["A"],     "hijos": ["D"]},
    "D": {"padres": ["B", "C"],"hijos": []}
}

def manto_de_markov(variable):
    """
    Calcula el Manto de Markov de una variable en la red.
    """
    padres = set(red_bayesiana[variable]["padres"])
    hijos = set(red_bayesiana[variable]["hijos"])
    co_padres = set()

    # Encontrar co-padres (otros padres de los hijos)
    for hijo in hijos:
        for p in red_bayesiana[hijo]["padres"]:
            if p != variable:
                co_padres.add(p)

    # Unir todos
    manto = padres.union(hijos).union(co_padres)
    return manto

# -------- DEMOSTRACIÓN --------

print("=== Ejemplo de Manto de Markov ===\n")

for var in red_bayesiana.keys():
    manto = manto_de_markov(var)
    print(f"Manto de Markov de {var}: {sorted(list(manto))}")

print("\nInterpretación:")
print("El manto de Markov de un nodo contiene toda la información que lo hace independiente del resto de la red.")
