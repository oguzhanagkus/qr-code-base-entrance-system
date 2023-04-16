import uuid


def generate(number_of_ids: int = 200, digit_count: int = 11) -> list:
    ids = []
    while len(ids) < number_of_ids:
        id_ = str(int(uuid.uuid4().hex, base=16))[:digit_count]
        if id not in ids:
            ids.append(id_)
    return ids
