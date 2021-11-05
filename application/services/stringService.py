from string import ascii_letters
from random import choices

def generateRandomString():
    return ''.join(choices(ascii_letters, k=10))
