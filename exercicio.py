# Código retirado da aula https://www.youtube.com/watch?v=RXWTvI7kBeU

import hashlib

data = "Exemplo de dado".encode("utf-8")
print(data)
hash_md5 = hashlib.md5(data).hexdigest()
print(hash_md5)

def  gerar_hash_arquivo(arquivo, algoritmo="md5"):
    hasher = hashlib.new(algoritmo)
    with open(arquivo, 'rb') as f:
        for bloco in iter(lambda: f.read(4096), b''):
            hasher.update(bloco)
    return hasher.hexdigest()

arquivo_atual = __file__
hash_arquivo = gerar_hash_arquivo(arquivo_atual)
print(hash_arquivo)