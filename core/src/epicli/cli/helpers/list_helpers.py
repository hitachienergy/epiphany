
def select_first(documents, query):
    if documents is not None:
        for x in documents:
            if query(x):
                return x
    return None


def select_all(documents, query):
    if documents is not None:
        result = list()
        for x in documents:
            if query(x):
                result.append(x)
        return result
    return None
