from hashids import Hashids

hashids = Hashids('balimate', 21)


def encode(id):
    result = hashids.encode(id)
    return result[0]


def decode(id):
    result = hashids.decode(id)
    return result[0]
