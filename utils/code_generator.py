import random
from datetime import datetime


def generate_unique_ids(box_count):
    """
    Generate a list of unique IDs.
    """
    unique_ids = {str(random.randint(100000000, 999999999)) for _ in range(box_count)}
    while len(unique_ids) < box_count:
        unique_ids.add(str(random.randint(100000000, 999999999)))
    return list(unique_ids)
