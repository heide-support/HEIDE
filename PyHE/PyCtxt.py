from PyHE import PyHE
from PyPtxt import PyPtxt

class PyCtxt:
    def __init__(self, pyHe, length):
        self.__keys = []
        if not isinstance(pyHe, PyHE):
            raise TypeError("pyPtxt init error: pyHE must be of type PyHE")
        if not isinstance(length, (int, long, float)):
            raise TypeError("pyPtxt init error: length not a number")

        self.__pyHE = pyHe
        self.__length = length
        return
    def __del__(self):
        self.__pyHE.delete(self)
    def getKeys(self):
        return self.__keys
    def appendKey(self, key):
        if not isinstance(key, str):
            raise TypeError("PyCtxt appendKey error: key must be a string")

        self.__keys.append(key)
    def getPyHE(self):
        return self.__pyHE
    def getLen(self):
        return self.__length


    ########################################################################
    # OPERATOR OVERRIDE METHODS #

    #####     SET OPERATOR     ######
    # '=' operator
    def set(self):
        return self.__pyHE.set(self)

    #####     STANDARD OPERATORS     ######
    # '+' operator
    def __add__(self, other):
        if not isinstance(other, (PyCtxt, int)):
            raise TypeError("PyCtxt '+' error: lhs must be of type PyCtxt or "
                            "int instead of " + str(type(other)))

        newCtxt = self.__pyHE.set(self)

        if isinstance(other, PyCtxt):
            newCtxt += other
        else:
            const_ctxt = self.__pyHE.encrypt(
                PyPtxt([other for _ in range(self.__length)],
                       self.__pyHE))

            newCtxt += const_ctxt

            del const_ctxt

        return newCtxt

    # '-' operator
    def __sub__(self, other):
        if not isinstance(other, PyCtxt):
            if not isinstance(other, (PyCtxt, int)):
                raise TypeError("PyCtxt '-' error: lhs must be of type PyCtxt or "
                            "int instead of " + str(type(other)))

        newCtxt = self.__pyHE.set(self)

        if isinstance(other, PyCtxt):
            newCtxt -= other
        else:
            const_ctxt = self.__pyHE.encrypt(
                PyPtxt([other for _ in range(self.__length)],
                       self.__pyHE))

            newCtxt -= const_ctxt

            del const_ctxt

        return newCtxt

    # '*' operator
    def __mul__(self, other):
        if not isinstance(other, (PyCtxt, int)):
            raise TypeError("PyCtxt '*' error: lhs must be of type PyCtxt or "
                            "int instead of " + str(type(other)))

        newCtxt = self.__pyHE.set(self)

        if isinstance(other, PyCtxt):
            newCtxt *= other
        else:
            const_ctxt = self.__pyHE.encrypt(
                PyPtxt([other for _ in range(self.__length)],
                       self.__pyHE))

            newCtxt *= const_ctxt

            del const_ctxt

        return newCtxt

    # negation operator
    def __neg__(self):
        newCtxt = self.__pyHE.set(self)

        newCtxt *= -1

        return newCtxt


    #####     IN-PLACE OPERATORS     ######

    # '+=' operator
    def __iadd__(self, other):
        if not isinstance(other, (PyCtxt, int)):
            raise TypeError("PyCtxt '+=' error: lhs must be of type PyCtxt"
                            " or int instead of type " + str(type(other)))

        if isinstance(other, PyCtxt):
            self.__pyHE.addCtxt(self, other, False)
        else:
            const_ctxt = self.__pyHE.encrypt(
                PyPtxt([other for _ in range(self.__length)],
                       self.__pyHE))

            self.__pyHE.addCtxt(self, const_ctxt, False)

            del const_ctxt

        return self

    # '-=' operator
    def __isub__(self, other):
        if not isinstance(other, (PyCtxt, int)):
            raise TypeError("PyCtxt '-=' error: lhs must be of type PyCtxt"
                            "or int instead of type " + str(type(other)))

        if isinstance(other, PyCtxt):
            self.__pyHE.addCtxt(self, other, True)
        else:
            const_ctxt = self.__pyHE.encrypt(
                PyPtxt([other for _ in range(self.__length)],
                       self.__pyHE))

            self.__pyHE.addCtxt(self, const_ctxt, True)

            del const_ctxt

        return self

    # '*=' operator
    def __imul__(self, other):
        if not isinstance(other, (PyCtxt, int)):
            raise TypeError("PyCtxt '*=' error: lhs must be of type PyCtxt"
                            " or int instead of type " + str(type(other)))

        if isinstance(other, PyCtxt):
            self.__pyHE.multiplyBy(self, other)
        else:
            const_ctxt = self.__pyHE.encrypt(
                PyPtxt([other for _ in range(self.__length)],
                       self.__pyHE))

            self.__pyHE.multiplyBy(self, const_ctxt)

            del const_ctxt

        return self

    # '==' operator
    def __eq__(self, other):
        if not isinstance(other, PyCtxt):
            raise TypeError("PyCtxt '==' error: lhs must be of type PyCtxt"
                            "instead of type " + str(type(other)))

        return self.__pyHE.equalsTo(self, other)

    # '!=' operator
    def __ne__(self, other):
        if not isinstance(other, PyCtxt):
            raise TypeError("PyCtxt '!=' error: lhs must be of type PyCtxt"
                            "instead of type " + str(type(other)))

        return not (self.__pyHE.equalsTo(self, other))


class PyCtxtLenError(Exception):
    def __init__(self):
        self.message = "Ciphertexts have mismatched lengths."