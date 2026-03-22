import hashlib

# Sinta-se livre para alterar a variável data e ver como o hash muda
# independente de quantos dos valores originais ainda restam.

data = "Exemplo de dado".encode("utf-8")
print(data)
hash_md5 = hashlib.md5(data).hexdigest()
print(hash_md5)