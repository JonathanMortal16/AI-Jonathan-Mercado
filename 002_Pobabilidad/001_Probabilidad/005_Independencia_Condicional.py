# Probabilidades de Lluvia
P_lluvia = 0.3
P_no_lluvia = 1 - P_lluvia  # 0.7

# Probabilidad de que alguien traiga paraguas dado lluvia / no lluvia
P_paraguas_dado_lluvia = 0.8       # Si llueve, la gente suele traer paraguas
P_paraguas_dado_no_lluvia = 0.1    # Si no llueve, casi nadie trae paraguas

# Probabilidad de piso mojado dado lluvia / no lluvia
P_pisoMojado_dado_lluvia = 0.9     # Si llueve, el piso casi siempre está mojado
P_pisoMojado_dado_no_lluvia = 0.05 # Si no llueve, casi nunca está mojado


# Queremos comparar:
#   P(PisoMojado | Lluvia, Paraguas)
#   vs
#   P(PisoMojado | Lluvia)


print("=== Condición: Está lloviendo (Lluvia = True) ===")
print("P(PisoMojado | Lluvia=True)                =", P_pisoMojado_dado_lluvia)
print("P(PisoMojado | Lluvia=True, Paraguas=True) =", P_pisoMojado_dado_lluvia)
print("P(PisoMojado | Lluvia=True, Paraguas=False)=", P_pisoMojado_dado_lluvia)
print()

print("=== Condición: NO está lloviendo (Lluvia = False) ===")
print("P(PisoMojado | Lluvia=False)                =", P_pisoMojado_dado_no_lluvia)
print("P(PisoMojado | Lluvia=False, Paraguas=True) =", P_pisoMojado_dado_no_lluvia)
print("P(PisoMojado | Lluvia=False, Paraguas=False)=", P_pisoMojado_dado_no_lluvia)
print()


