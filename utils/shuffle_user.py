import random


def arrange_secret_santa(user_ids):
    """
    This Function creates USer id Pairs for Secret Santa

    Parameters : list of ids
    return : dictionary of pairs id

    """
    # Make a copy of the list and shuffle it
    shuffled_ids = user_ids[:]
    random.shuffle(shuffled_ids)

    # Arrange in pairs (A gives to B, B gives to C, ..., last gives to A)
    pairings = {
        shuffled_ids[i]: shuffled_ids[(i + 1) % len(shuffled_ids)]
        for i in range(len(shuffled_ids))
    }

    return pairings


# user_ids = [1, 2, 3, 4, 5]  # Example user IDs
# pairings = arrange_secret_santa(user_ids)
# print(pairings)
# for giver, receiver in pairings.items():
#     print(f"User {giver} will give a gift to User {receiver}")
