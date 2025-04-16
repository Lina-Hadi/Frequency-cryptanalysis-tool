import re
from collections import Counter
from math import gcd
from functools import reduce
import streamlit as st

# Fréquences des lettres en français
freq_fr = {
    'A': 0.0842, 'B': 0.0106, 'C': 0.0334, 'D': 0.0366, 'E': 0.1715, 'F': 0.0106, 'G': 0.0097,
    'H': 0.0077, 'I': 0.0753, 'J': 0.0054, 'K': 0.0012, 'L': 0.0577, 'M': 0.0297, 'N': 0.0713,
    'O': 0.0531, 'P': 0.0295, 'Q': 0.0136, 'R': 0.0662, 'S': 0.0795, 'T': 0.0722, 'U': 0.0632,
    'V': 0.0152, 'W': 0.0001, 'X': 0.0046, 'Y': 0.0030, 'Z': 0.0013
}

def clean_text(text):
    """Nettoie le texte en gardant uniquement les lettres majuscules"""
    return re.sub(r'[^A-Z]', '', text.upper())

# ------------ Mono-Alphabétique : César ------------
def lettre_en_index(l):
    """Convertit une lettre en son index dans l'alphabet (A=0, B=1, etc.)"""
    return ord(l) - ord('A')

def MonoAlphabetique(texte):
    """Détermine le décalage pour un chiffrement César basé sur l'analyse fréquentielle"""
    texte = clean_text(texte)
    texte_counter = Counter(texte)
    total_lettres = sum(texte_counter.values())
    
    if total_lettres == 0:
        return 0
        
    # Calcul des fréquences pour chaque lettre du texte
    frequences = {lettre: texte_counter[lettre] / total_lettres for lettre in texte_counter}
    
    # Recherche de la lettre la plus fréquente (probablement 'E' en français)
    lettre_plus_frequente = max(frequences, key=frequences.get)
    
    # Calcul du décalage en supposant que la lettre la plus fréquente est 'E'
    decalage = (lettre_en_index(lettre_plus_frequente) - lettre_en_index('E')) % 26
    
    return decalage

def decrypt_cesar(texte, decalage):
    """Déchiffre un texte avec le chiffrement César selon le décalage donné"""
    resultat = ""
    for lettre in texte:
        if lettre.isalpha():
            # Préserve la casse
            if lettre.isupper():
                new = chr((ord(lettre) - ord('A') - decalage) % 26 + ord('A'))
            else:
                new = chr((ord(lettre) - ord('a') - decalage) % 26 + ord('a'))
            resultat += new
        else:
            # Préserve les caractères non alphabétiques
            resultat += lettre
    return resultat

# ------------ Vigenère : Encryption, Attack ------------
def encrypt_vigenere(text, key):
    """Chiffre un texte avec le chiffrement de Vigenère"""
    clean_text_input = clean_text(text)
    key = clean_text(key)  # Assurez-vous que la clé est propre
    
    if not key:
        return "La clé ne peut pas être vide"
        
    encrypted = ''
    key_length = len(key)
    
    for i, char in enumerate(clean_text_input):
        shift = ord(key[i % key_length]) - ord('A')
        encrypted += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        
    return encrypted

def find_repeated_sequences(text, min_length=3, max_length=20):
    """Trouve les séquences répétées dans le texte"""
    sequences = {}
    distances = []
    
    # Recherche de séquences de différentes longueurs
    for length in range(min_length, min(max_length + 1, len(text) // 2)):
        for i in range(len(text) - length + 1):
            seq = text[i:i + length]
            if seq in sequences:
                # Nouvelle occurrence de cette séquence
                distances.append(i - sequences[seq][-1])
            sequences.setdefault(seq, []).append(i)
    
    # Filtrer pour ne garder que les séquences qui apparaissent plusieurs fois
    meaningful_distances = [d for d in distances if d > 0]
    return meaningful_distances

def pgcd_multiple(numbers):
    """Calcule le PGCD de plusieurs nombres"""
    if not numbers:
        return None
    return reduce(gcd, numbers)

def find_key_length_with_pgcd(text, min_length=3, max_length=20):
    """Trouve la longueur probable de la clé avec la méthode de Kasiski"""
    distances = find_repeated_sequences(text, min_length, max_length)
    
    if not distances:
        return None
    
    # Collecter les PGCD par paires
    pgcd_counts = {}
    for i in range(len(distances)):
        for j in range(i + 1, len(distances)):
            pair_pgcd = gcd(distances[i], distances[j])
            if pair_pgcd > 1:  # Ignore les PGCD de 1
                pgcd_counts[pair_pgcd] = pgcd_counts.get(pair_pgcd, 0) + 1
    
    if not pgcd_counts:
        return None
    
    # Trouver le PGCD le plus fréquent
    return max(pgcd_counts.items(), key=lambda x: x[1])[0]

def split_text(text, length):
    """Divise le texte en 'length' sous-textes"""
    chunks = [''] * length
    for i, char in enumerate(text):
        chunks[i % length] += char
    return chunks

def chi_squared(observed, expected):
    """Calcule le chi-carré entre les fréquences observées et attendues"""
    chi2 = 0
    for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        obs = observed.get(char, 0)
        exp = expected.get(char, 0)
        if exp > 0:  # Évite la division par zéro
            chi2 += ((obs - exp) ** 2) / exp
    return chi2

def find_key_char(chiffre):
    """Trouve la lettre clé la plus probable pour un sous-texte donné"""
    best_key = 'A'  # Valeur par défaut
    best_chi2 = float('inf')
    n = len(chiffre)
    
    if n == 0:
        return best_key
        
    for key_val in range(26):
        key_char = chr(key_val + ord('A'))
        decrypted = decrypt_chiffre(chiffre, key_char)
        
        # Compter les fréquences des lettres dans le texte déchiffré
        freqs = Counter(decrypted)
        observed = {char: freqs.get(char, 0) / n for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}
        
        # Calculer le chi-carré avec les fréquences théoriques
        chi2 = 0
        for char in freq_fr:
            expected = freq_fr[char] * n
            if expected > 0:  # Évite la division par zéro
                chi2 += ((freqs.get(char, 0) - expected) ** 2) / expected
        
        if chi2 < best_chi2:
            best_chi2 = chi2
            best_key = key_char
            
    return best_key

def decrypt_chiffre(chiffre, key_char):
    """Déchiffre un fragment avec une seule lettre de clé (comme César)"""
    key_val = ord(key_char) - ord('A')
    return ''.join(chr((ord(c) - ord('A') - key_val) % 26 + ord('A')) for c in chiffre)

def find_key(text, key_length):
    """Trouve la clé complète pour le chiffrement de Vigenère"""
    chiffres = split_text(text, key_length)
    return ''.join(find_key_char(chiffre) for chiffre in chiffres)

def decrypt_vigenere(text, key):
    """Déchiffre un texte avec le chiffrement de Vigenère"""
    if not key:
        return "La clé ne peut pas être vide"
        
    text = clean_text(text)
    key = clean_text(key)
    
    decrypted = ''
    key_length = len(key)
    
    for i, char in enumerate(text):
        shift = ord(key[i % key_length]) - ord('A')
        decrypted += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        
    return decrypted

def indice_de_coincidence(text):
    """Calcule l'indice de coïncidence d'un texte"""
    n = len(text)
    if n <= 1:
        return 0
        
    freqs = Counter(text)
    ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
    return ic

def estimate_key_length_by_ic(text, max_key_len=20):
    """Estime la longueur de la clé par l'indice de coïncidence"""
    text = clean_text(text)
    target_ic = 0.074  # Indice de coïncidence théorique pour le français
    best_len = 1
    best_diff = float('inf')
    
    for key_len in range(1, min(max_key_len + 1, len(text) // 2)):
        chunks = split_text(text, key_len)
        ics = [indice_de_coincidence(chunk) for chunk in chunks if len(chunk) > 1]
        
        if ics:
            avg_ic = sum(ics) / len(ics)
            diff = abs(avg_ic - target_ic)
            
            if diff < best_diff:
                best_diff = diff
                best_len = key_len
                
    return best_len

# ------------ Interface Streamlit ------------
def main():
    st.set_page_config(page_title="Analyse Cryptographique", layout="wide")
    st.title("Outil de Déchiffrement Cryptographique")

    analyse_choice = st.sidebar.radio("Choisissez le type d'analyse:",
        ["Déchiffrement Mono-alphabétique (César)", "Déchiffrement Poly-alphabétique (Vigenère)"])

    if analyse_choice == "Déchiffrement Mono-alphabétique (César)":
        st.header("Déchiffrement de César")
        text_input = st.text_area("Texte chiffré:", height=150)
        
        if st.button("Analyser et Déchiffrer"):
            if not text_input:
                st.error("Veuillez entrer un texte.")
            else:
                decalage = MonoAlphabetique(text_input)
                decrypted = decrypt_cesar(text_input, decalage)
                st.subheader(f"Décalage estimé: {decalage}")
                st.text_area("Texte déchiffré:", decrypted, height=150)
                
                # Afficher aussi des alternatives pour les 3 décalages les plus probables
                st.subheader("Alternatives possibles:")
                for i in range(1, 4):
                    alt_decalage = (decalage + i) % 26
                    alt_decrypted = decrypt_cesar(text_input, alt_decalage)
                    st.text(f"Décalage {alt_decalage}: {alt_decrypted[:100]}..." if len(alt_decrypted) > 100 else alt_decrypted)

    else:
        st.header("Déchiffrement Vigenère")
        vigenere_input = st.text_area("Texte chiffré:", height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            method = st.radio("Méthode d'analyse:", ["Kasiski", "Indice de Coïncidence"])
        with col2:
            manual_key = st.text_input("Clé manuelle (facultatif):")

        if st.button("Analyser et Déchiffrer"):
            if not vigenere_input:
                st.error("Veuillez entrer un texte.")
            else:
                clean_cipher = clean_text(vigenere_input)
                
                if len(clean_cipher) < 20:
                    st.error("Texte trop court pour une analyse fiable.")
                else:
                    if manual_key:
                        # Utiliser la clé fournie manuellement
                        key = clean_text(manual_key)
                        decrypted = decrypt_vigenere(clean_cipher, key)
                        st.success(f"Déchiffrement avec la clé: {key}")
                    else:
                        # Détection automatique de la clé
                        key_length = find_key_length_with_pgcd(clean_cipher) if method == "Kasiski" else estimate_key_length_by_ic(clean_cipher)
                        
                        if not key_length or key_length <= 1:
                            st.warning("Échec de la détection de la longueur de la clé. Essai avec différentes longueurs...")
                            
                            # Essayer avec plusieurs longueurs de clé possibles
                            possible_lengths = range(2, 8)
                            for length in possible_lengths:
                                key = find_key(clean_cipher, length)
                                decrypted = decrypt_vigenere(clean_cipher, key)
                                st.text(f"Longueur {length}, clé: {key}")
                                st.text_area(f"Déchiffrement (longueur {length}):", decrypted[:200], height=100)
                        else:
                            key = find_key(clean_cipher, key_length)
                            decrypted = decrypt_vigenere(clean_cipher, key)
                            st.success(f"Clé estimée: {key} (longueur: {key_length})")
                            st.text_area("Texte déchiffré:", decrypted, height=150)

if __name__ == "__main__":
    main()