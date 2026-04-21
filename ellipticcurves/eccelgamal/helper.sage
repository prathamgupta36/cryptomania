from random import getrandbits, choice
from string import ascii_uppercase, digits

def generateMessage(N: int) -> str: 
    return ''.join(choice(ascii_uppercase + digits) for _ in range(N))

def messageToInt(message: str) -> int: 
    return int((message.encode('utf-8')).hex(), 16)

def encrypt(m, Qa, G): 
    k = getrandbits(128) # ephemeral key
    s = m*G # map message onto curve via base point 
    c1 = k*G
    c2 = s + k*Qa
    return c1, c2

def decrypt(c1, c2, na): 
    return c2 - na*c1