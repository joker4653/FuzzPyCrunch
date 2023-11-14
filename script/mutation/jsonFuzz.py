import random
import json
import sys

randVals = [-1000000,-5,-4,-3,-2,-1,0,1, 2, 3, "a", "b", "c", 10000000, sys.maxsize, -sys.maxsize - 1]
# account for the json object type, by ensuring we keep valid structure
class mutateJSON:
    'Mutaton strategies which are unique to JSON'
    def __init__(self, fileformat, corpus) -> None:
        self.fileFormat = fileformat
        self.currentCoverage = 0
        self.lengthModifier = 1
        self.corpus = json.loads(corpus)

        self.mutationFunctions = [
            self.mutateValues,
            self.addPairs,
            self.deletePairs,
            self.deepNesting,
            self.objectDup,
            self.typeConf
        ]



    def chooseMutation(self, corpus):
        mut = random.choice(self.mutationFunctions)
        return mut(corpus)
    

    def mutateValues(self, corpus):
        'messes up keys to be unexpected values and types'
        dictJson = json.loads(corpus)
        key_to_update = random.choice(list(dictJson.keys()))
        dictJson[key_to_update] = random.choice(randVals)
        print(dictJson)
        return json.dumps(dictJson)



    def addPairs(self, corpus):
        'add additional pairs to input'
 
        dictJson = json.loads(corpus)
        for i in range(0, random.randint(1, 1000)):
            key = str(random.choice(randVals))
            value = random.choice(randVals)
            dictJson[key] = value

        return json.dumps(dictJson)

        
    def deletePairs(self, corpus):

        dictJson = json.loads(corpus)
        key_to_delete = random.choice(list(dictJson.keys()))
        del dictJson[key_to_delete]
        print(dictJson)
        return json.dumps(dictJson)
    

    
    def deepNesting(self, corpus):
        """ Mutation strategy to deeply nest the JSON object """
        # Randomly choose a depth for nesting
        depth = random.randint(2, 500)
        
        # Function to create nested structure
        def create_nest(obj, currentDepth):
            if currentDepth == depth:
                return obj  # Return the final nested object
            else:
                return create_nest({"nested": obj}, currentDepth + 1)
        
        # Apply the nesting to the original corpus and convert to JSON string
        nestedObject = create_nest(json.loads(corpus), 1)
        return json.dumps(nestedObject)
    


    def objectDup(self, corpus):
        """ Mutation strategy to duplicate entire objects within the JSON """
        depth = random.randint(2,500)
        def duplicateObject(obj, currDepth):

            if currDepth == depth:
                return obj
            else:

                if isinstance(obj, dict):
                    # Duplicate the object and recursively apply duplication
                    duplicated = {key: duplicateObject(value) for key, value in obj.items()}
                    print(obj)
                    return json.dumps({**duplicated, **duplicated})  # Merge the duplicated dictionary with itself
                elif isinstance(obj, list):
                    # Duplicate each element in the list
                    print(obj)
                    duplicatedList = [duplicateObject(element) for element in obj]
                    return json.dumps(duplicatedList + duplicatedList)  # Concatenate the duplicated list with itself
                else:
                    # failsafe but should always be either list or dict
                    return obj

        return duplicateObject(corpus, 1)
    

    def typeConf(self, corpus):
        vals = json.loads(corpus)

        if isinstance(vals, dict):
            return json.dumps(list(vals))
        else:
            return json.dumps(dict(vals))
