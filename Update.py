import hashlib

h = hashlib.sha256()

# É possível adicionar dados aos poucos, o que é bem útil 
# ao lidar com grandes volumes de dados

h.update(b"Dado parte 1")
h.update(b"Dado parte 2")
h.update(b"Dado parte 3")

print(h.hexdigest())