import random

def generate_password(length: int):
    """
    Generates a random password of a given length.
    Args:
        length (int): The length of the password to be generated.
    Returns:
        str: A randomly generated password consisting of uppercase letters, lowercase letters, and digits.
    """

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = ""
    for i in range(length):
        password += random.choice(chars)
    return password