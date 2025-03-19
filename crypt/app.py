from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

# Generate the key for substitution cipher
chars = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)
key = chars.copy()
random.shuffle(key)

# Substitution Cipher
def substitution_encrypt(plain_text):
    cipher_text = ""
    for letter in plain_text:
        index = chars.index(letter)
        cipher_text += key[index]
    return cipher_text

def substitution_decrypt(cipher_text):
    plain_text = ""
    for letter in cipher_text:
        index = key.index(letter)
        plain_text += chars[index]
    return plain_text

# Caesar Cipher
def caesar_encrypt(plain_text, shift=3):
    cipher_text = ""
    for letter in plain_text:
        if letter in chars:
            index = chars.index(letter)
            cipher_text += chars[(index + shift) % len(chars)]
        else:
            cipher_text += letter
    return cipher_text

def caesar_decrypt(cipher_text, shift=3):
    plain_text = ""
    for letter in cipher_text:
        if letter in chars:
            index = chars.index(letter)
            plain_text += chars[(index - shift) % len(chars)]
        else:
            plain_text += letter
    return plain_text

# Vigenère Cipher
def vigenere_encrypt(plain_text, key):
    cipher_text = ""
    key_length = len(key)
    for i, letter in enumerate(plain_text):
        if letter in chars:
            shift = chars.index(key[i % key_length])
            index = chars.index(letter)
            cipher_text += chars[(index + shift) % len(chars)]
        else:
            cipher_text += letter
    return cipher_text

def vigenere_decrypt(cipher_text, key):
    plain_text = ""
    key_length = len(key)
    for i, letter in enumerate(cipher_text):
        if letter in chars:
            shift = chars.index(key[i % key_length])
            index = chars.index(letter)
            plain_text += chars[(index - shift) % len(chars)]
        else:
            plain_text += letter
    return plain_text

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# API route for encryption
@app.route("/encrypt", methods=["POST"])
def encrypt_message():
    data = request.json
    plain_text = data.get("message")
    encryption_type = data.get("type")
    key = data.get("key", "")  # Key for Vigenère Cipher

    if encryption_type == "substitution":
        cipher_text = substitution_encrypt(plain_text)
    elif encryption_type == "caesar":
        cipher_text = caesar_encrypt(plain_text)
    elif encryption_type == "vigenere":
        cipher_text = vigenere_encrypt(plain_text, key)
    else:
        return jsonify({"error": "Invalid encryption type"}), 400

    return jsonify({"cipher_text": cipher_text})

# API route for decryption
@app.route("/decrypt", methods=["POST"])
def decrypt_message():
    data = request.json
    cipher_text = data.get("message")
    encryption_type = data.get("type")
    key = data.get("key", "")  # Key for Vigenère Cipher

    if encryption_type == "substitution":
        plain_text = substitution_decrypt(cipher_text)
    elif encryption_type == "caesar":
        plain_text = caesar_decrypt(cipher_text)
    elif encryption_type == "vigenere":
        plain_text = vigenere_decrypt(cipher_text, key)
    else:
        return jsonify({"error": "Invalid encryption type"}), 400

    return jsonify({"plain_text": plain_text})

if __name__ == "__main__":
    app.run(debug=True)