# Probabilidades base
P_A = 0.3                     # 30% prob. de que esté lloviendo
P_B_given_A = 0.9             # Si llueve, 90% que el suelo esté mojado
P_B_given_notA = 0.1          # Si NO llueve, 10% que el suelo esté mojado (por otras causas)
P_C_given_A_B = 0.95          # Si llueve y suelo mojado, 95% que la persona lleve paraguas
P_C_given_notA_B = 0.6        # Si no llueve pero suelo mojado (ej: regaron), 60% que lleve paraguas
P_C_given_notA_notB = 0.05    # Si ni llueve ni hay agua, solo 5% lleva paraguas

# 1) Escenario 1: Lluvia, suelo mojado, persona con paraguas
P_A_B_C = P_A * P_B_given_A * P_C_given_A_B
print(f"P(A,B,C) = P(A)*P(B|A)*P(C|A,B) = {P_A_B_C:.5f}")

# 2) Escenario 2: No llueve, suelo mojado (porque lavaron), persona con paraguas
P_notA_B_C = (1 - P_A) * P_B_given_notA * P_C_given_notA_B
print(f"P(~A,B,C) = P(~A)*P(B|~A)*P(C|~A,B) = {P_notA_B_C:.5f}")

# 3) Escenario 3: No llueve, suelo seco, persona sin paraguas
P_notA_notB_notC = (1 - P_A) * (1 - P_B_given_notA) * (1 - P_C_given_notA_notB)
print(f"P(~A,~B,~C) = P(~A)*P(~B|~A)*P(~C|~A,~B) = {P_notA_notB_notC:.5f}")
