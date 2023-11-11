import random
from mutations import *


# account for csv type, including headers to keep inputs somewhat reasonable
class mutateCSV(mutator):
    def __init__(self, fileformat, corpus, rows=None, columns=None) -> None:
        self.fileFormat = fileformat
        self.currentCoverage = 0
        self.lengthModifier = 1
        self.corpus = corpus # not delimited yet 
    
    def chooseMutation(self, corpus):
        rand = random.randint(0,2)
        newMut = str(0)
        if rand == 0:
            newMut = self.lineOverflow(corpus)
        elif rand == 1:
            newMut = self.mutateDelimeters(corpus)
        elif rand == 2:
            newMut = self.integerOverflowFields(corpus)

        return newMut
        
    def lineOverflow(self, corpus):
        self.lengthModifier = self.lengthModifier + 1
        return corpus * self.lengthModifier
        

    def mutateDelimeters(self, corpus):
        return str(0)

    def integerOverflowFields(self, corpus):
        return str(0)
