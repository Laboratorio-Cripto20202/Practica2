import math
from utils import *

import numpy.matlib 
import numpy.linalg
import numpy as np 

class Hill():

    def __init__(self, alphabet, n, key=None):
        """
        Constructor de clase, recibiendo un alfabeto completamente necesario pero
        podría no recibir una llave de cifrado, en cuyo caso, hay que generar una,
        para el caso del tamañHo de la llave, hay que asegurarse que tiene raíz entera.
        :param alphabet: una cadena con todos los elementos del alfabeto.
        :param n: el tamaño de la llave, obligatorio siempre.
        :param key: una cadena que corresponde a la llave, en caso de ser una llave inválida
        arrojar una CryptographyException.
        """
        self.alphabet = alphabet
        sqrt_perfect = math.sqrt(n)
        if ((sqrt_perfect-int(sqrt_perfect)) == 0):
            self.keyLength = n
            if (key is None):
                self.key = newHillKey(n)
                self.keyMatrix = self.makeMatrix()
                det = np.linalg.det(self.keyMatrix)

                while inverse(det,len(alphabet)) is None:
                    self.key = newHillKey(n)
                    self.keyMatrix = self.makeMatrix()
                    det = np.linalg.det(self.keyMatrix)
            else:
                self.key = key
                self.keyMatrix = self.makeMatrix()
        else:
            raise CryptographyException()

        #if inverse(np.linalg.det(self.keyMatrix),len(self.alphabet)) is None:
        #    raise CryptographyException()
        

    def makeMatrix(self):
        """
        Transforma la llave en un matriz, para ejecutar el algoritmo de Hill
        :return: Matriz que representa a la llave del algoritmo
        """
        #cuadrado: raíz cuadrada de la lontitud de la palabra clave
        cuadrado = int(math.sqrt(self.keyLength))
        
        #Creamos su equivalente en su posición en el alfabeto
        llaveNums = []
        for l in list(self.key):
            llaveNums.append(self.alphabet.index(l))
        
        #Convertimos la palabra clave en una matriz de cuadradoxcuadrado
        llaveNums = np.array([llaveNums])
        llaveNums = np.reshape(llaveNums,(cuadrado,cuadrado))
        return llaveNums

    def cofactores(self):
        """
        Obtiene la matriz de cofactores de la matriz que representa a la llave
        :return: Matriz de cofactores
        """
        matrix = self.keyMatrix
        C = np.zeros(matrix.shape)
        nrows, ncols = C.shape
        for row in range(nrows):
            for col in range(ncols):
                minor = matrix[np.array(list(range(row)) + list(range(row+1,nrows)))[:,np.newaxis],
                            np.array(list(range(col)) + list(range(col+1,ncols)))]
                C[row, col] = (-1)**(row+col) * np.linalg.det(minor)
        return C

    def makeInverseMatrix(self):
        """
        Obtiene la matriz inversa de aquella que representa a la palabra clave
        :return: Matriz que representa a la matriz inversa de la llave del algoritmo
        """
        len_alphabet = len(self.alphabet) 

        det = np.linalg.det(self.keyMatrix)

        factor1 = inverse(int(round(det)),len_alphabet)
        factor2 = self.cofactores().T
        inversa = self.operation_to_matrix(factor2, lambda i: i * factor1)

        return inversa

    def makeVector(self,word):
        """
        Transforma una palabra en un vector, para poder utilizarse con la palabra clave en forma de matriz
        :param word: Palabra a convertir en vector
        :return: Vector que contiene a la palabra
        """
        word = list(word)
        #cuadrado de la longitud de la palabra clave
        cuadrado = int(math.sqrt(self.keyLength))
        #completamos la palabra para que la longitud sea multiplo del cuadrado de la llave
        if len(word) % cuadrado != 0:
            word = word + ([self.alphabet[0]] * (cuadrado - (len(word) % cuadrado)))

        #Creamos su equivalente en su posición en el alfabeto
        wordNums = []
        for l in word:
            wordNums.append(self.alphabet.index(l))

        #Lo volvemos un vector de n/cuadrado filas y cuadrado columnas
        wordNums = np.array([wordNums])
        wordNums = np.reshape(wordNums, (math.ceil(len(word) / cuadrado), cuadrado))
        return wordNums

    def operation_to_matrix(self,matrix,operation):
        """
        Aplica una operación a cada uno de los elementos de la matriz
        :param matriz: Matriz sobre la cual se realizará la operación.
        :param operation: Operación a ejecutar sobre los elementos de la matriz.
        :return: Matriz transformada de acuerdo a la operación.
        """
        vectorize_operation =  np.vectorize(operation)
        return vectorize_operation(matrix)

    def cifrar_descifrar(self,matrix,cadena):
        """
        Aplica el algoritmo de cifrado o descifrado con respecto al criptosistema de Hill. El modo lo determina la matriz.
        :param matriz: Llave de cifrado o descifrado del mensaje.
        :param cadena: El mensaje a transformar, ya sea para cifrarla o descifrarla.
        :return: Mensaje cifrado o mensaje, claro, dependiendo del modo.
        """
        #Tamaño del alfabeto
        len_alphabet = len(self.alphabet) 
        #quitamos espacios de la palabra a cifrar
        cadena = cadena.replace(" ","")
        #Lo hacemos vector
        mensaje = self.makeVector(cadena)

        cifrado = []
        cadenaCifrada = ""

        #Por cada fragmento de mensaje
        for i in range(mensaje.shape[0]):
            fragmento = np.array([mensaje[i]])
            #Creamos la transpuesta, y tenemos una matriz de nx1, donde n es la longitud del fragmento
            fragmento = fragmento.T
            #Multiplicamos la transpuesta del fragmento del mensaje, con la clave; y sacamos el módulo
            res = self.operation_to_matrix(np.dot(matrix,fragmento),lambda i: i % len_alphabet)
            
            #Pasamos de nuevo a una matriz de 1xn
            res = np.reshape(res,(1,res.shape[0]))[0]

            #Guardamos el fragmento cifrado en una lista
            for item in res:
                cifrado.append(self.alphabet[int(round(item)) % len_alphabet])

        for elem in cifrado:
            cadenaCifrada += elem
        return cadenaCifrada


    def cipher(self, message):
        """
        Aplica el algoritmo de cifrado con respecto al criptosistema de Hill, el cual recordando
        que todas las operaciones son mod |alphabet|.
        :param message: El mensaje a enviar que debe ser cifrado.
        :return: Un criptotexto correspondiente al mensaje, este debe de estar en representación de
        cadena, no lista.
        """
        return self.cifrar_descifrar(self.keyMatrix,message)
        
        


    def decipher(self, ciphered):
        """
        Usando el algoritmo de decifrado, recibiendo una cadena que se asegura que fue cifrada
        previamente con el algoritmo de Hill, obtiene el texto plano correspondiente.
        :param ciphered: El criptotexto de algún mensaje posible.
        :return: El texto plano correspondiente a manera de cadena.
        """
        llaveDes = self.makeInverseMatrix()
        return self.cifrar_descifrar(llaveDes,ciphered)

    