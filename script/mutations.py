# mutation logic

import random
import json
import csv

class mutator:
    'Base Mutation Class with Default strategies'
    def __init__(self, fileformat, corpus) -> None:
        self.fileFormat = fileformat
        self.currentCoverage = 0
        self.lengthModifier = 1
        self.corpus = corpus
    
    def bitFlip(self, corpus):
                    return str(0)


    def byteFlip(self, corpus):
        flips = random.randint(1,len(corpus))


        flipped_string = ""
        for i in range(0, flips):
            byteToFlip = random.randint(0,len(corpus) - 1)
            # Get the ASCII code of the character
            ascii_code = ord(corpus[byteToFlip])
            
            # Bitwise NOT operation (bit flip)
            flipped_ascii_code = ~ascii_code & 0xFF  # Ensure it's an 8-bit value
            
            # Convert the flipped ASCII code back to a character
            flipped_char = chr(flipped_ascii_code)
            
            flipped_string += flipped_char

        return flipped_string

    def keywordExtraction(self, corpus):
                return str(0)


    def magicNumAbuse(self, corpus):
                return str(0)

    def CoverageBasedMutation(self, corpus):
                return str(0)


    def validateInput(self, corpus):
                return str(0)


    def lengthAbuse(self, corpus):
        self.lengthModifier = self.lengthModifier + 1
        return corpus + "A" * self.lengthModifier
    
    
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

    



# account for the json object type, by ensuring we keep valid structure
class mutateJSON(mutator):
    'Mutaton strategies which are unique to JSON'
    def __init__(self, fileformat, corpus) -> None:
        self.fileFormat = fileformat
        self.currentCoverage = 0
        self.lengthModifier = 1
        self.corpus = json.loads(corpus)

    def chooseMutation(self, corpus):
        rand = random.randint(0,2)
        newMut = str(0)
        if rand == 0:
            newMut = self.mutateValues(corpus)
        elif rand == 1:
            newMut = self.addPairs(corpus)
        elif rand == 2:
            newMut = self.deletePairs(corpus)

        return newMut
    

    def mutateValues(self, corpus):
        'messes up keys to be unexpected values and types'
        dictJson = json.loads(corpus)
        key_to_update = random.choice(list(dictJson.keys()))
        dictJson[key_to_update] = random.choice([-1000000,-5,-4,-3,-2,-1,0,1, 2, 3, "a", "b", "c", 10000000])

        return json.dumps(dictJson)



    def addPairs(self, corpus):
        'add additional pairs to input'
 
        dictJson = json.loads(corpus)
        key = str(random.randint(-1000, 1000))
        value = random.choice([-1000000,-5,-4,-3,-2,-1,0,1, 2, 3, "a", "b", "c", 10000000])
        dictJson[key] = value

        return json.dumps(dictJson)

        
    def deletePairs(self, corpus):

        dictJson = json.loads(corpus)
        key_to_delete = random.choice(list(dictJson.keys()))
        del dictJson[key_to_delete]

        return json.dumps(dictJson)

        

class mutateJPEG(mutator):
    def validateInput():
        pass


class mutateELF(mutator):
    def validateInput():
        pass


class mutatePDF(mutator):
    def validateInput():
        pass