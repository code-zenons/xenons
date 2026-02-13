import asyncio
from rich.console import Console
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

console = Console()

class BifrostChat:
    def __init__(self):
        self.priv_key = ec.generate_private_key(ec.SECP256R1())
        self.pub_key = self.priv_key.public_key()
        self.shared_key = None

    def get_pub_key_bytes(self):
        return self.pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def derive_secret(self, peer_pub_bytes):
        peer_pub = serialization.load_pem_public_key(peer_pub_bytes)
        shared = self.priv_key.exchange(ec.ECDH(), peer_pub)
        self.shared_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'bifrost-handshake'
        ).derive(shared)
        console.print("[green]Secure Channel Established (AES-256-GCM Ready)[/green]")

    def encrypt(self, msg):
        if not self.shared_key: return None
        aes = AESGCM(self.shared_key)
        nonce = os.urandom(12)
        ct = aes.encrypt(nonce, msg.encode(), None)
        return nonce + ct

    def decrypt(self, data):
        if not self.shared_key: return None
        aes = AESGCM(self.shared_key)
        nonce = data[:12]
        ct = data[12:]
        return aes.decrypt(nonce, ct, None).decode()
