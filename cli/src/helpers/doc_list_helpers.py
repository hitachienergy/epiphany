
class ExpectedSingleResultException(Exception):
    """Raised when the query returns none or too many results."""
    pass


def select_first(documents, query):
    if documents is not None:
        for x in documents:
            if query(x):
                return x
    return None


def select_all(documents, query):
    if documents is not None:
        result = []
        for x in documents:
            if query(x):
                result.append(x)
        return result
    return None


def select_single(documents, query):
    if documents is not None:
        results = select_all(documents, query)
        elements_count = len(results)
        if elements_count == 1:
            return results[0]
        raise ExpectedSingleResultException("Expected one element but received: " + str(elements_count))
    return None
