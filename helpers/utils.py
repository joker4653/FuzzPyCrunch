from io import StringIO
import re
import json
import csv
from mutations import *


# bytes which will when added cause integer overflows and funky stuff
magicbytes = []


def checkfileFormat(sampleInput):
    
    if checkJson(sampleInput) == True:
        return 'json'
    
    if checkCSV(sampleInput) == True:
        return 'csv'

    return None

def checkJson(sampleInput):
    try:
        json.loads(sampleInput)
        return True
    except:
        return False


def checkCSV(sampleInput):
    try:
        csv_file = StringIO(sampleInput)
        csv.reader(csv_file)
        return True
    except csv.Error:
        return False




def factory(fileFormat, ValidInputs):
    format = checkfileFormat(ValidInputs)


    if format == "json":
        return mutateJSON(fileFormat, ValidInputs)
    elif format == "csv":
        return mutateCSV(fileFormat, ValidInputs)
    else:
        # return None on unable to identify file format / plaintext
        return mutator("unknown", ValidInputs)



# Bunch of regex crap to detect different formats

JSONRegex = ""


XMLRegex = ""


CSVRegex = ""


JPEGRegex = ""


