# mutation logic

import random
import json
import csv

class mutator:
    'Base Mutation Class with Generic strategies'
    def __init__(self, fileformat, corpus) -> None:
        self.fileFormat = fileformat
        self.currentCoverage = 0
        self.lengthModifier = 1
        self.corpus = corpus
    
    def nullInput(self, corpus):
        return ""

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
            newMut = self.nullInput(corpus)
        elif rand == 5:
            newMut = self.magicNumAbuse(corpus)
        elif rand == 6:
            newMut = self.CoverageBasedMutation(corpus)
        else:
            newMut = self.lengthAbuse(corpus)

        return newMut
    