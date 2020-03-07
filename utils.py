import random 
import string

class CryptographyException(Exception):

    def __init__(self):
        self.message = "Invalid key"

    def __str__(self):
        return self.message
    

#Genera una nueva llave de Hill
def newHillKey (size):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(size))