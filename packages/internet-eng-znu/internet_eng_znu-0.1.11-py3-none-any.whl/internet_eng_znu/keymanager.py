from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
import os

class KeyManager:
    def __init__(self, public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public_key.pem")):
        self.public_key_path = public_key_path
        self.public_key = self.load_public_key()

    def load_public_key(self):
        with open(self.public_key_path, 'rb') as f:
            return serialization.load_pem_public_key(f.read(), backend=default_backend())

    def encrypt_message(self, message):
        ciphertext = self.public_key.encrypt(
            message.encode(),  # Convert message to bytes
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        url_safe_base64 = base64.urlsafe_b64encode(ciphertext).decode('utf-8')
        return url_safe_base64
