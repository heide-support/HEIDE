from PyHE import PyHE

class PyPtxt:
    def __init__(self, ptxt, pyHe):
        if not isinstance(ptxt, list):
            raise TypeError("pyPtxt init error: ptxt must be of type list")
        if not isinstance(pyHe, PyHE):
            raise TypeError("pyPtxt init error: pyHE must be of type PyHE")

        self.__ptxt = ptxt
        self.__pyHe = pyHe
        self.__length = len(ptxt)
        self.__numSlots = pyHe.numSlots()
        n = max(1, self.__numSlots)
        self.__ptxtList = [ptxt[i:i + n] for i in range (0, self.__length, n)]
        return

    def numSlots(self):
        return self.__numSlots

    def numPtxt(self):
        return len(self.__ptxtList)

    def getPtxtList(self):
        return self.__ptxtList

    def getPyHE(self):
        return self.__pyHe

    def getPtxtLen(self):
        return self.__length
