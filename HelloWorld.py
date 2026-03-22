import hashlib

texto = 'Olá, Matrix'

# É necessário 'encodar' a string para bytes antes

hash_md5 = hashlib.md5(texto.encode()).hexdigest()
hash_sha1 = hashlib.sha1(texto.encode()).hexdigest()
hash_sha256 = hashlib.sha256(texto.encode()).hexdigest()

print(f"MD5: {hash_md5}")
print(f"SHA5: {hash_sha1}")
print(f"SHA256 {hash_sha256}")

#Lembrando aqui que:

# MD5 é recomendado para Checksums simples (NÃO USE PARA SENHAS)
  #Checksum é "um código númerico ou alfanumérico gerado por um algoritmo, funcionando como
  # uma "impressão digital" para garantir a integridade de dados e arquivos"

# SHA1 é legado (EVITAR USAR EM SEGURANÇA)

# SHA256 é de uso geral, integridade de dados, ele e o SHA512