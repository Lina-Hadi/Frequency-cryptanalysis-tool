frequences_fr = {
    'E': 0.147, 'A': 0.078, 'I': 0.075, 'S': 0.073, 'N': 0.071, 'R': 0.070,
    'T': 0.070, 'O': 0.053, 'L': 0.052, 'U': 0.045, 'D': 0.036, 'C': 0.033,
    'M': 0.029, 'P': 0.027, 'V': 0.016, 'Q': 0.013, 'F': 0.012, 'B': 0.011,
    'G': 0.010, 'H': 0.010, 'J': 0.003, 'X': 0.003, 'Y': 0.002, 'Z': 0.001,
    'K': 0.000, 'W': 0.000
}
from collections import Counter
import matplotlib.pyplot as plt

def lettre_en_index(l):
    return ord(l) - ord('A')

def MonoAlphabetique(texte):

  #on enleve les espaces + on met en majuscule
  texte=texte.replace(' ','').upper()
  texte = Counter(texte)
  #counter cest une fonction qui creer un dictionnaire de combien de fois chaque lettre apparait dans une phrase
  #exemple : texte = {'H': 1, 'E': 1, 'L': 2, 'O': 1}

  total_lettres = sum(texte.values())
  #texte.values par exemple [1,1,2,1] ensuite sum de ca ca va nous donner 5

  #frquence des lettres => f= nombre apparition/total
  frequences = {}
  for lettre in texte:
    frequences[lettre] = texte[lettre] / total_lettres
    #texte dico
    #print(texte[lettre])

  #maintenant on va chercher la lettre la plus frequente DANS MON TEXTE
  #get() recupere la valeur associé a la clé
  #donc on recup la frequence max basé sur les frequences mashi la lettre
  lettre_plus_frequente = max(frequences, key=frequences.get)
  print("Lettre la plus fréquente dans le texte :", lettre_plus_frequente)

  #on va trouver le decalage
  #on se base sur E psk elle est la plus repeté en francais

  Decalage = (lettre_en_index(lettre_plus_frequente) - lettre_en_index('E')) % 26  #lettre en index transforme la lettre en index lol
  print("Décalage trouvé :", Decalage)

  return Decalage, frequences





def decrypt(texte,decalage):
  resultat=""
  for lettre in texte :
    if lettre.isalpha():
      #juste pourconfirmer si c une lettre
      new = chr((ord(lettre) - ord('A') - decalage) % 26 + ord('A'))
      resultat+=new
      #- ord(A) pour travailler su l'alphabet et ensuite on fait le decalage , ensuite on rajoute l'ord A pr revenir a ascii
      #pour eviter les caracteres speciaux sur les bords si A par exemple -decalage bah on aura un symbole      resultat+=new
    else:
      resultat+=lettre
  print('le resultat est :',resultat)
  return resultat




# TEST

Text = "WKH HDJOH KDV ODQGHG"
dec, frequences_txt = MonoAlphabetique(Text)
decrypt(Text, dec)