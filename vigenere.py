import random

class Vigenere():
    
    def __init__(self, alphabet, password=None):
        #Recomendación, ingeniárselas para no cargar siempre O(n^2) en memoria aunque esto no
        #será evaluado, con n el tamaño del alfabeto.
        """
        Constructor de clase, recibe un parámetro obligatorio correspondiente al alfabeto
        y un parámetro opcional que es la palabra clave, en caso de ser None, entonces
        generar una palabra pseudoaleatoria de al menos tamaño 4.
        :param alphabet: Alfabeto a trabajar con el cifrado.
        :param password: El password que puede ser o no dada por el usuario.
        """
        self.alphabet=alphabet
        self.password = []
        if not password is None:
            for i in range(len(password)):
                self.password.append(alphabet.find(password[i]))    
        else:
            for i in range(0,random.randint(4, 10)):
                self.password.append(alphabet[random.randint(0,27)])
        return

    def cipher(self, message):
        """
        Usando el algoritmo de cifrado de vigenere, cifrar el mensaje recibido como parámetro,
        usando la tabla descrita en el PDF.
        :param message: El mensaje a cifrar.
        :return: Una cadena de texto con el mensaje cifrado.
        """
        solution= ""
        for i in range(len(message)):
            solution += self.alphabet[(self.alphabet.find(message[i])+self.password[i%len(self.password)])% 27]
        return solution
            


    def decipher(self, ciphered):
        """
        Implementación del algoritmo de decifrado, según el criptosistema de vigenere.
        :param ciphered: El criptotexto a decifrar.
        :return: El texto plano correspondiente del parámetro recibido.
        """
        solution= ""
        for i in range(len(ciphered)):
            solution += self.alphabet[(self.alphabet.find(ciphered[i])-self.password[i%len(self.password)])% 27]
        return solution