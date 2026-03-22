import hashlib
import os

# Exercício retirado de https://www.youtube.com/watch?v=RXWTvI7kBeU
# Salt na prática
# O Salt é gerado aleatóriamente então a cada print o seu salt será diferente.

salt = os.urandom(16)
senha = 'minhasenha'.encode("utf-8")
hash_com_salt = hashlib.pbkdf2_hmac('sha256', senha, salt, 1000)
print(hash_com_salt.hex()) 