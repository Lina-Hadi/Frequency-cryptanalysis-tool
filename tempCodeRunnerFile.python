import re
import math
from collections import Counter
from math import gcd
from functools import reduce

# Fréquences en français des lettres
freq_fr = {
    'A': 0.0842, 'B': 0.0106, 'C': 0.0334, 'D': 0.0366, 'E': 0.1715, 'F': 0.0106, 'G': 0.0097,
    'H': 0.0077, 'I': 0.0753, 'J': 0.0054, 'K': 0.0012, 'L': 0.0577, 'M': 0.0297, 'N': 0.0713,
    'O': 0.0531, 'P': 0.0295, 'Q': 0.0136, 'R': 0.0662, 'S': 0.0795, 'T': 0.0722, 'U': 0.0632,
    'V': 0.0152, 'W': 0.0001, 'X': 0.0046, 'Y': 0.0030, 'Z': 0.0013
}

def clean_text(text):
    """Nettoyer le texte pour ne garder que les lettres majuscules"""
    return re.sub(r'[^A-Z]', '', text.upper())

def encrypt_vigenere(text, key):
    """Chiffrer un texte avec Vigenère"""
    clean_text_input = clean_text(text)
    encrypted = ''
    key_index = 0
    key_length = len(key)
    
    for char in clean_text_input:
        key_char = key[key_index % key_length]
        shift = ord(key_char) - ord('A')
        encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        encrypted += encrypted_char
        key_index += 1
    
    return encrypted

def find_repeated_sequences(text, min_length=3):
    """Trouver les séquences répétées dans le texte (Test de Kasiski)"""
    sequences = {}
    for i in range(len(text) - min_length):
        seq = text[i:i + min_length]
        if seq in sequences:
            sequences[seq].append(i)
        else:
            sequences[seq] = [i]
    
    # Filtrer les séquences répétées et calculer les distances
    repeated = {seq: positions for seq, positions in sequences.items() if len(positions) > 1}
    
    # Calculer les distances entre occurrences
    distances = []
    for seq, positions in repeated.items():
        if len(positions) > 1:
            print(f"Séquence '{seq}' trouvée aux positions: {positions}")
            for i in range(len(positions) - 1):
                distance = positions[i + 1] - positions[i]
                distances.append(distance)
    
    return distances


def pgcd_multiple(numbers):
    """Calculer le PGCD de plusieurs nombres"""
    if not numbers:
        return None
    
    # Utiliser la réduction fonctionnelle avec gcd comme fonction binaire
    return reduce(gcd, numbers)

def find_key_length_with_pgcd(text):
    """Estimer la longueur de la clé en utilisant le PGCD des distances"""
    # Trouver les répétitions
    distances = find_repeated_sequences(text)
    
    if not distances:
        return None
    
    print(f"Distances trouvées: {distances}")
    
    # Calculer le PGCD de toutes les distances
    key_length = pgcd_multiple(distances)
    
    # Si le PGCD est 1, essayer d'éliminer les distances problématiques
    if key_length == 1:
        print("PGCD global égal à 1, tentative d'analyse plus fine...")
        
        # Création d'un dictionnaire qui compte la fréquence des facteurs communs
        pgcd_counts = {}
        
        # Analyser les PGCD par paire
        for i in range(len(distances)):
            for j in range(i+1, len(distances)):
                pair_pgcd = gcd(distances[i], distances[j])
                if pair_pgcd > 1:  # Ne comptabiliser que les PGCD utiles
                    if pair_pgcd in pgcd_counts:
                        pgcd_counts[pair_pgcd] += 1
                    else:
                        pgcd_counts[pair_pgcd] = 1
        
        # Si nous avons trouvé des PGCD pertinents
        if pgcd_counts:
            # Trouver le PGCD le plus fréquent
            best_pgcd = max(pgcd_counts.items(), key=lambda x: x[1])[0]
            print(f"PGCD les plus fréquents par paires: {pgcd_counts}")
            print(f"PGCD retenu: {best_pgcd}")
            key_length = best_pgcd
        else:
            print("Impossible de trouver un PGCD pertinent autre que 1.")
    
    print(f"Longueur de clé estimée: {key_length}")
    return key_length

def split_text(text, length):
    """Diviser le texte en chiffres selon la longueur de la clé"""
    chiffres = [''] * length
    for i, char in enumerate(text):
        chiffres[i % length] += char
    return chiffres

def decrypt_chiffre(chiffre, key_char):
    """Déchiffrer un chiffre avec une clé"""
    decrypted = ''
    key_val = ord(key_char) - ord('A')
    for char in chiffre:
        dec = (ord(char) - ord('A') - key_val) % 26
        decrypted += chr(dec + ord('A'))
    return decrypted

def find_key_char(chiffre):
    """Trouver le caractère de clé pour un chiffre en utilisant l'analyse de fréquence"""
    best_chi2 = float('inf')
    best_key = None
    
    # Calculer les fréquences observées
    n = len(chiffre)
    observed_freq = Counter(chiffre)
    
    # Tester chaque décalage possible
    for key_val in range(26):
        key_char = chr(key_val + ord('A'))
        decrypted = decrypt_chiffre(chiffre, key_char)
        
        # Calculer le chi-carré pour ce décalage
        chi2 = 0
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            expected = freq_fr[char] * n
            observed = decrypted.count(char)
            chi2 += (observed - expected) ** 2 / expected if expected > 0 else 0
        
        if chi2 < best_chi2:
            best_chi2 = chi2
            best_key = key_char
    
    return best_key


def find_key(text, key_length):
    """Trouver la clé complète en analysant chaque chiffre"""
    chiffres = split_text(text, key_length)
    key = ''
    for i, chiffre in enumerate(chiffres):
        key_char = find_key_char(chiffre)
        key += key_char
        print(f"Caractère {i+1} de la clé: {key_char}")
    return key

def decrypt_vigenere(text, key):
    """Déchiffrer un texte chiffré avec Vigenère"""
    decrypted = ''
    key_index = 0
    key_length = len(key)
    
    for char in text:
        key_char = key[key_index % key_length]
        shift = ord(key_char) - ord('A')
        decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        decrypted += decrypted_char
        key_index += 1
    
    return decrypted

def attack_vigenere(ciphertext):
    """Fonction principale d'attaque sur le chiffre de Vigenère - uniquement avec Kasiski"""
    clean_cipher = clean_text(ciphertext)
    
    print("Analyse du texte chiffré avec le test de Kasiski...")
    key_length = find_key_length_with_pgcd(clean_cipher)
    
    if not key_length:
        print("Impossible de déterminer la longueur de la clé. Test de Kasiski échoué.")
        return None, None
    
    print(f"\nLongueur de clé retenue (selon Kasiski): {key_length}")
    
    # Trouver la clé
    print("\nRecherche de la clé par analyse fréquentielle...")
    key = find_key(clean_cipher, key_length)
    print(f"Clé complète trouvée: {key}")
    
    # Déchiffrer
    decrypted = decrypt_vigenere(clean_cipher, key)
    return key, decrypted

# Exemple concret
if __name__ == "__main__":
    # Texte clair original en français
    plain_text = """
    La cryptographie est l'étude des techniques permettant de chiffrer des messages
    c'est à dire de les rendre inintelligibles sans une action spécifique. Cette 
    discipline comprend aussi l'analyse de la robustesse des méthodes de chiffrement
    face aux tentatives pour les rendre inefficaces. Le chiffre de Vigenère est un 
    système de chiffrement par substitution polyalphabétique, inventé par Blaise de
    Vigenère au seizième siècle. Il utilise une clé qui détermine comment chaque lettre
    du message sera chiffrée, contrairement au chiffre de César qui utilise un décalage
    fixe. Le test de Kasiski est une méthode d'analyse qui permet de déterminer
    la longueur de la clé utilisée dans le chiffre de Vigenère.
    """
    
    # Clé de chiffrement
    original_key = "CRYPTOGRAPHIE"
    
    print(f"Texte original: \n{plain_text[:100]}...\n")
    print(f"Clé utilisée pour le chiffrement: {original_key}\n")
    
    # Chiffrer le texte
    ciphertext = encrypt_vigenere(plain_text, original_key)
    print(f"Texte chiffré: \n{ciphertext[:100]}...\n")
    
    print("=== DÉBUT DE L'ATTAQUE ===")
    
    # Lancer l'attaque
    found_key, decrypted_text = attack_vigenere(ciphertext)
    
    print("\n=== RÉSULTATS ===")
    print(f"Clé originale: {original_key}")
    print(f"Clé trouvée: {found_key}")
    print(f"\nTexte déchiffré (premiers 200 caractères):\n{decrypted_text[:200]}...")
    
    # Vérifier le succès
    if found_key == original_key:
        print("\nSuccès ! La clé a été correctement retrouvée.")
    else:
        print("\nLa clé trouvée diffère de l'originale, mais le texte déchiffré peut quand même avoir du sens.")