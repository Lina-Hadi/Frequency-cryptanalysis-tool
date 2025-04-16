# Frequency Cryptanalysis Tool - Streamlit App

Welcome to our cryptanalysis application for classical ciphers!

This interactive tool was designed to help decrypt texts encrypted with monoalphabetic (Caesar) and polyalphabetic (Vigenère) methods. It applies statistical analysis, including:

- Index of Coincidence (IC),
- Frequency Analysis (Chi²),
- Key Length Detection,
- Automatic Ciphertext Decryption.

---

## 💡 Features

- Graphical interface using **Streamlit**.
- Supports encrypted text with or without spaces.
- Automatic key detection using Index of Coincidence.
- Smart key reduction to avoid repeated patterns (e.g., "VIGENEREVIGENERE" ➡️ "VIGENERE").
- Clear result display for easy interpretation.

---

## 🧠 How to Use

1. **Run the application**

```bash
streamlit run app.py
```

2. **Input Encrypted Text**

Copy/paste your ciphertext into the input area labeled "Enter your encrypted text".

3. **Click "Analyze Text"**

- The key will be automatically estimated.
- The ciphertext will be decrypted.
- Results will be displayed in the interface.

---

## 🔧 Dependencies

- Python 3.x
- streamlit

Quick install:

```bash
pip install streamlit
```

---

## 💻 Example

**Encrypted Text:**
```
GIIVLTKSBZGTUMVINBRXHHVHZAZIPLEMLCKWCIIQZBZEAXUIXPOJSVVVYMYQRWJEBMY...
```

**Expected Output:**
```
Key Found: VIGENERE
Decrypted Text: LACRYPTOGRAPHIEESTLETUDEDESTECHNIQUESPERMETTANTDECHIFFRERDESMESSAGES...
```

---

## 👥 Team

Project developed by:

- Adjissi Fatima Amina
- Hadi Meriem Lina
- Mellaz Maya Melissa
- Moulai Tinhinane

---

## ⚠️ Notes

- Works best with French texts.
- Accents and punctuation are automatically removed during analysis.

---

## 🚀 Coming Soon

- Kasiski test support.
- Graphical representation of letter frequencies.

---

Thanks for using our tool!

#crypto #streamlit #vigenere #cesar #frequencyanalysis

