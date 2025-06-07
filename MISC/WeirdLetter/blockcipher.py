# Substitution table
from collections import Counter


substitution = {
    "a":"q",
    "b":"e",
    "c":"z",
    "d":"g",
    "e":"v",
    "f":"c",
    "g":"f",
    "h":"k",
    "i":"h",
    "j":"u",
    "k":"p",
    "l":"t",
    "m":"r",
    "n":"x",
    "o":"j",
    "p":"o",
    "q":"s",
    "r":"w",
    "s":"i",
    "t":"l",
    "u":"n",
    "v":"d",
    "w":"a",
    "x":"b",
    "y":"m",
    "z":"y",
}

def frequency_analysis(text):
    text = text.lower()
    letters_only = [char for char in text if char.isalpha()]
    return Counter(letters_only)


# Encrypted text (paste your full ciphertext here)
with open('letter.txt', 'r') as file:
    ciphertext = file.read().strip()

    # Decrypt
    plaintext = ""
    for char in ciphertext:
        if char.lower() in substitution:
            new_char = substitution[char.lower()]
            plaintext += new_char.upper() if char.isupper() else new_char
        else:
            plaintext += char
    
    with open('decrypted_letter.txt', 'w') as output_file:
        output_file.write(plaintext)

frequency = frequency_analysis(ciphertext)
# Print frequency analysis
print("Frequency Analysis:")
for letter, count in frequency.most_common():
    print(f"{letter}: {count}")
# Output decrypted text
print(plaintext[:100])
