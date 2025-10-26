# Lo que el agente cree antes de observar nada
P_lluvia = 0.3        # 30% de probabilidad de que llueva hoy
P_no_lluvia = 1 - P_lluvia  # 70% de probabilidad de que NO llueva

# Supongamos que el agente aún no ha visto el clima
print("Probabilidad a priori (antes de observar):")
print("P(lluvia)     =", P_lluvia)
print("P(no lluvia)  =", P_no_lluvia)
print()

# Ahora el agente observa un dato (por ejemplo, cielo nublado)
# Pero todavía no aplica Bayes; solo anota la observación.
observacion = "Cielo nublado"

print("Observación recibida:", observacion)
print("Aún no se actualizan las creencias (solo priors).")
print()
