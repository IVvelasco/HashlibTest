import hashlib
import random

a = 'a'
b = 'b'
c = 'c'
d = 'd'

letra = random.choice([a, b, c, d])

hash_md5 = hashlib.md5(letra.encode()).hexdigest()
hash_sha1 = hashlib.sha1(letra.encode()).hexdigest()
hash_sha256 = hashlib.sha256(letra.encode()).hexdigest()

print(f"MD5: {hash_md5}")
print(f"SHA1: {hash_sha1}")
print(f"SHA256: {hash_sha256}")