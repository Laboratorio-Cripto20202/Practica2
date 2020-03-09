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

def inverse(a, n):
    """
    Encuentra el inverso multiplicativo del numero dado, . 
    Parámetro:
        a -- el numero al cual se le quiere encontrar el
            inverso multiplicativo.
        n -- el tamanio del alfabeto
    """
    
    t, newT = 0, 1
    r, newR = n, a

    while (newR != 0):
        q = r // newR
        t, newT = newT, t - q * newT 
        r, newR = newR, r - q * newR

    if (r != 1): 
        return None #No tiene inverso multiplicativo
    if (t < 0):
        t = t + n

    return t