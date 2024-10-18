from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def generate_private_key():
    return ec.generate_private_key(ec.SECP256R1())

def generate_public_key(private_key):
    return private_key.public_key()

def encrypt_text(public_key, text):
    encrypted = public_key.encrypt(text, ec.ECDH(), HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=None))
    return encrypted

def decrypt_text(crypted_text, private_key):
    crypted_text = private_key.decrypt(crypted_text,ec.ECDH(),HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=None))
    return crypted_text