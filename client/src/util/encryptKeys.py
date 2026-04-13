from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization


class encryptor:
    def __init__(self):
        self.__privateKey = rsa.generate_private_key(
            public_exponent=65537, # this is the standard for the public_exponent
            key_size=4096,
        )
        self.publicKey = self.__privateKey.public_key()
        
    def decrypt(self, data):
        print(len(data))
        print(self.__privateKey.key_size // 8)
        plaintext = self.__privateKey.decrypt(
            data,
            padding.PKCS1v15()
        )
        return plaintext
    
    def getPublicKeyPEM(self): #pem is the format that can be transfered to react so it can encrypt with
        return self.publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    @property
    def getPublicKey(self):
        return self.publicKey

if __name__ == '__main__':
    e = encryptor()
    print(e.getPublicKeyPEM())