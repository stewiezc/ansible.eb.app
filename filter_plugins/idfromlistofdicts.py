def idfromlistofdicts(l):
    result = []
    for item in l:
        result.append(item['id'])


    return result


class FilterModule(object):
    def filters(self):
        return {
            'idfromlistofdicts': idfromlistofdicts,
        }