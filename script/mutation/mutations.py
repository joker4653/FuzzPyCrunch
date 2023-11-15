# mutation logic

import random
import json
import csv
import string
class mutator:
    'Base Mutation Class with Generic strategies'
    def __init__(self, fileformat, corpus) -> None:
        self.fileFormat = fileformat
        self.currentCoverage = 0
        self.lengthModifier = 1
        self.corpus = corpus
    

        self.mutationFunctions = [
            self.nullInput,
            self.bitFlip,
            self.byteFlip,
            self.lengthAbuse

        ]


    def chooseMutation(self, corpus):
        mut = random.choice(self.mutationFunctions)
        return mut(corpus)

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


    def lengthAbuse(self, corpus):
        self.lengthModifier = self.lengthModifier + 1
        if self.lengthModifier == 20:
            self.lengthModifier = 0
        return corpus + "A" * self.lengthModifier
    
    
    def formatString(self,corpus):
        # %s will dereference memory if there is a format string vuln.
        pass

    def randomCharsAndNums(self, corpus):
        pass