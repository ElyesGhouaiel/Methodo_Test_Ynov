def additionner(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Les deux arguments doivent être des nombres (int ou float).")
    return a + b

def est_pair(nombre):
    if not isinstance(nombre, int):
        raise TypeError("Le paramètre doit être un entier.")
    return nombre % 2 == 0

def valider_email(email):
    if not isinstance(email, str):
        raise TypeError("L'email doit être une chaîne de caractères.")
    if "@" not in email or "." not in email:
        return False
    return True

def calculer_moyenne(notes):
    if not isinstance(notes, list):
        raise TypeError("L'argument doit être une liste.")
    if not all(isinstance(note, (int, float)) for note in notes):
        raise ValueError("Toutes les notes doivent être des nombres.")
    if len(notes) == 0:
        return 0
    return sum(notes) / len(notes)

def convertir_temperature(celsius):
    if not isinstance(celsius, (int, float)):
        raise TypeError("La température doit être un nombre.")
    return (celsius * 9/5) + 32
