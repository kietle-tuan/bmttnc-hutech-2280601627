from .alphabet import ALPHABET

class CaeserCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def encrypt_text(self, plain_text, key):
        encrypted = ""
        for char in plain_text.lower():
            if char in self.alphabet:
                idx = (self.alphabet.index(char) + key) % 26
                encrypted += self.alphabet[idx]
            else:
                encrypted += char
        return encrypted

    def decrypt_text(self, cipher_text, key):
        decrypted = ""
        for char in cipher_text.lower():
            if char in self.alphabet:
                idx = (self.alphabet.index(char) - key) % 26
                decrypted += self.alphabet[idx]
            else:
                decrypted += char
        return decrypted