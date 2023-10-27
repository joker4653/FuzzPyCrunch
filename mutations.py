# mutation logic

import random


class mutator:
    def __init__(self, fileformat) -> None:
        self.fileFormat = fileformat
        self.currentCoverage = 0
    
    def bitFlip(self, corpus):
                    return str(0)


    def byteFlip(self, corpus):
        flips = random.randint(1,len(corpus))

        for i in range(0, flips):
            byteToFlip = random.randint(0,len(corpus) - 1)
            corpus[byteToFlip] ^ random.choice([1, 2, 4, 8, 16, 32, 64])

        return corpus

    def keywordExtraction(self, corpus):
                return str(0)


    def magicNumAbuse(self, corpus):
                return str(0)

    def CoverageBasedMutation(self, corpus):
                return str(0)


    def validateInput(self, corpus):
                return str(0)


    def lengthAbuse(corpus):
        return corpus + "A" * random.randint(1,512)
    
    def chooseMutation(self, corpus):
        rand = random.randint(1,7)
        newMut = str(0)
        if rand == 1:
            newMut = self.bitFlip(corpus)
        elif rand == 2:
            newMut = self.byteFlip(corpus)
        elif rand == 3:
            newMut = self.keywordExtraction(corpus)
        elif rand == 4:
            newMut = self.magicNumAbuse(corpus)
        elif rand == 5:
            newMut = self.magicNumAbuse(corpus)
        elif rand == 6:
            newMut = self.CoverageBasedMutation(corpus)
        else:
            newMut = self.lengthAbuse(corpus)

        return newMut

class mutateXML(mutator):
    def validateInput():
        pass



class mutateCSV(mutator):
    def validateInput():
        pass    


class mutateJSON(mutator):
    def validateInput():
        pass
        

class mutateJPEG(mutator):
    def validateInput():
        pass


class mutateELF(mutator):
    def validateInput():
        pass


class mutatePDF(mutator):
    def validateInput():
        pass