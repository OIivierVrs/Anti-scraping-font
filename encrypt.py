import json
import base64
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from dotenv import main
main.load_dotenv()

def encrypt_file(font_name, i = 1):

    encrypted_font_name = os.getenv("FONTS_FOLDER") + 'encrypted/' + font_name + '_' + str(i) + '_Encrypted'

    font_mapping = json.load(open(encrypted_font_name + '.json'))

    font_file_path = encrypted_font_name + '.bin'

    key = bytes(os.getenv("ENCRYPT_KEY"), 'utf-8')

    # Generate a random initialization vector (IV) of length 16
    iv = os.urandom(16)

    # Convert dictionary to JSON string
    data = json.dumps(font_mapping).encode('utf-8')

    # Pad the data to be a multiple of 16 bytes (AES block size) using PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Create AES cipher with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Encrypt the data
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Base64 encode the encrypted data and IV
    encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')
    iv_b64 = base64.b64encode(iv).decode('utf-8')

    # Write encrypted data and IV to a file
    with open(font_file_path, 'w') as f:
        f.write(encrypted_data_b64 + '\n')
        f.write(iv_b64 + '\n')