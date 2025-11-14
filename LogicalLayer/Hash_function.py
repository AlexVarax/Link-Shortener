import xxhash

class Hash:
    def __init__(self):
        pass

    def hash(self, id, word: str):
        return str(xxhash.xxh32(word, seed = id%2147483648).hexdigest())

h = Hash
print(h.hash(h, 3, "dsad"))