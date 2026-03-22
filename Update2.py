import hashlib

dados_completos = hashlib.sha256(b"Dado parte 1 dado parte 2 dado parte 3")
print(dados_completos.hexdigest())