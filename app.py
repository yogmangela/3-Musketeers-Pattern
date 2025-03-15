from flask import Flask, render_template, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

app = Flask(__name__)

# AES key and IV setup (same as before)
SECRET_KEY = os.urandom(32)  # 32 bytes for AES-256
IV = os.urandom(16)  # Initialization Vector for CBC mode

# AES encryption function
def encrypt_text(plain_text):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(IV + encrypted_data).decode('utf-8')

# AES decryption function
def decrypt_text(encrypted_text):
    encrypted_data = base64.b64decode(encrypted_text)
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plain_text = unpadder.update(decrypted_data) + unpadder.finalize()
    return plain_text.decode('utf-8')

@app.route('/')
def home():
    return render_template('index.html')  # This renders the index.html file

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    text_to_encrypt = data.get("text", "")
    if text_to_encrypt:
        encrypted_text = encrypt_text(text_to_encrypt)
        return jsonify({"encrypted_text": encrypted_text}), 200
    else:
        return jsonify({"error": "No text provided"}), 400

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    encrypted_text = data.get("encrypted_text", "")
    if encrypted_text:
        try:
            decrypted_text = decrypt_text(encrypted_text)
            return jsonify({"decrypted_text": decrypted_text}), 200
        except Exception as e:
            return jsonify({"error": "Decryption failed", "message": str(e)}), 400
    else:
        return jsonify({"error": "No encrypted text provided"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# from flask import Flask
# import os

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Hello, Docker!"

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)