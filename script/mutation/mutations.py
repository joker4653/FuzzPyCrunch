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
            self.lengthAbuse,
            self.formatString,
            self.randomCharsAndNums

        ]


    def chooseMutation(self, corpus):
        mut = random.choice(self.mutationFunctions)
        return mut(corpus)

    def nullInput(self, corpus):
        return ""

    def bitFlip(self, corpus):
        if not corpus:
            return corpus

        # Convert the string to a bytearray for in-place modification
        byte_array = bytearray(corpus, 'utf-8')
        #pick random byte
        byte_index = random.randint(0, len(byte_array) - 1)

        # Choose a random bit to flip (0-7 for a single byte)
        bit_index = random.randint(0, 7)

        # xor
        byte_array[byte_index] ^= (1 << bit_index)

        # Convert the bytearray back to a string and return it
        try:
            # Attempt to decode the modified bytearray back to a string
            return byte_array.decode('utf-8')
        except UnicodeDecodeError:
            # In case of a decoding error (invalid byte sequence), return the original string
            return corpus


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
        return corpus * self.lengthModifier
    
    
    def formatString(self,corpus):
        # %s will dereference memory if there is a format string vuln. and cause seg fault
        return "%10s %20s %50s\n %100s %1000s" * self.lengthModifier

    def randomCharsAndNums(self, corpus):
        """ 
        permutation of alphanumeric characters of random length 
        at a random position in the input string.
        """
        # Generate a random length for the permutation
        permutationLength = random.randint(1, 10)

        # Generate a random permutation of alphanumeric characters
        permutation = ''.join(random.choices(string.ascii_letters + string.digits, k=permutationLength))

        # Choose a random position to insert the permutation
        index = random.randint(0, len(corpus))

        # Insert the permutation into the input string
        return corpus[:index] + permutation + corpus[index:]