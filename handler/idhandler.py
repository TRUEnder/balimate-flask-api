from hashids import Hashids

hashids = Hashids('balimate', 21)


def encode(id):
    result = hashids.encode(id)
    if (len(result) == 0):
        response = {
            'code': 'fail',
            'error': {
                'code': 'Data not found'
            }
        }
        return response

    else:
        response = {
            'code': 'success',
            'data': result[0]
        }
        return response


def decode(id):
    result = hashids.decode(id)
    if (len(result) == 0):
        response = {
            'code': 'fail',
            'error': {
                'code': 'Data not found'
            }
        }
        return response

    else:
        response = {
            'code': 'success',
            'data': result[0]
        }
        return response
