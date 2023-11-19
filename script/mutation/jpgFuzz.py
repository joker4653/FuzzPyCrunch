import random
import struct

class mutateJPEG:
    """Class containing JPEG specific mutation methods"""
    def __init__(self, fileformat, corpus, rows=None, columns=None) -> None:
        self.fileFormat = fileformat
        self.currentCoverage = 0
        self.lengthModifier = 1
        self.corpus = corpus 
    
        self.mutationFunctions = [
            self.headerManipulation,
            self.randomByteInsertion,
            self.eofTruncation,
            self.segmentLengthModification,
            self.criticalSegmentRemoval,
            self.arbitraryByteValueChanges,
        ]

    def chooseMutation(self, corpus):
        mut = random.choice(self.mutationFunctions)
        return mut(corpus)

    def headerManipulation(self, corpus):
        """ Randomly modify values in the JPEG file header. """
        byteArray = bytearray(corpus)
        if len(corpus) > 20:  # Ensuring there's enough corpus to manipulate
            position = random.randint(2, 20)  # Avoid modifying the SOI marker
            byteArray[position] = random.randint(0, 255)
        return bytes(byteArray)

    def randomByteInsertion(self, corpus):
        """ Insert random bytes at a random position in the corpus"""
        position = random.randint(0, len(corpus))
        random_byte = random.randint(0, 255)
        return corpus[:position] + bytes([random_byte]) + corpus[position:]

    def eofTruncation(self, corpus):
        """ Truncate the file at a random position before the actual end"""
        if len(corpus) > 1:
            position = random.randint(1, len(corpus))
            return corpus[:position]
        return corpus

    def segmentLengthModification(self, corpus):
        """Randomly change the length fields in various segments"""
        if len(corpus) > 4:  # Ensuring there's enough corpus to manipulate
            position = random.randint(2, len(corpus) - 2)
            length = struct.pack('>H', random.randint(0, 255))  # New random length
            corpus = corpus[:position] + length + corpus[position + 2:]
        return corpus

    def criticalSegmentRemoval(self, corpus):
        """Remove a random segment from the corpus"""
        if len(corpus) > 4:
            position = random.randint(2, len(corpus) - 2)
            end_position = corpus.find(b'\xff', position + 2)
            if end_position != -1:
                corpus = corpus[:position] + corpus[end_position:]
        return corpus

    def arbitraryByteValueChanges(self, corpus):
        """Modify byte values at random positions"""

        bytes = bytearray(corpus)
        for i in range(random.randint(1, (len(corpus)// 2))):   
            if len(corpus) > 0:
                position = random.randint(0, len(corpus) - 1)
                bytes[position] = random.randint(0, 255)
        return bytes


