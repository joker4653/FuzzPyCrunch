import random
from mutations import *



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
        for i in range(0, random.randint(1, 1000)):
            key = str(random.randint(-10000, 10000))
            value = random.choice([-1000000,-5,-4,-3,-2,-1,0,1, 2, 3, "a", "b", "c", 10000000])
            dictJson[key] = value

        return json.dumps(dictJson)

        
    def deletePairs(self, corpus):

        dictJson = json.loads(corpus)
        key_to_delete = random.choice(list(dictJson.keys()))
        del dictJson[key_to_delete]

        return json.dumps(dictJson)