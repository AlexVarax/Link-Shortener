from xxhash import xxh32 

class Hash:
    def __init__(self):
        pass

    def hash(self, id, word: str):
        return str(xxh32(word, seed = id%2147483648).hexdigest())