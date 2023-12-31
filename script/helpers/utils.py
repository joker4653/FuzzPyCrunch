from io import StringIO
from io import BytesIO

import re
import json
import csv
from PIL import Image
import xml.etree.ElementTree as ET
from mutation.mutations import *
from mutation.csvFuzz import *
from mutation.elfFuzz import *
from mutation.jpgFuzz import *
from mutation.jsonFuzz import *
from mutation.pdfFuzz import *
from mutation.xmlFuzz import *

# bytes which will when added cause integer overflows and funky stuff
magicbytes = []


def checkfileFormat(sampleInput):
    
    if checkJson(sampleInput) == True:
        return 'json'
    
    if checkXML(sampleInput) == True:
        return 'xml'

    if checkCSV(sampleInput) == True:
        return 'csv'

    if checkJPEG(sampleInput) == True:
        return 'jpeg'
    
    return None

def checkJson(sampleInput):
    try:
        json.loads(sampleInput)
        return True
    except:
        return False


def checkCSV(sampleInput):
    if isinstance(sampleInput, bytes):
        return False
    try:
        csvFile = StringIO(sampleInput)
        csv.reader(csvFile)
        return True
    except csv.Error:
        return False

def checkXML(sampleInput):
    if isinstance(sampleInput, bytes):
        return False
    try:
        xmlFile = ET.fromstring(sampleInput)
        return True
    except:
        return False

def checkJPEG(sampleInput):
    try:

        with Image.open(BytesIO(sampleInput)) as img:
            return True
    except:
        return False

def factory(fileFormat, ValidInputs):
    format = checkfileFormat(ValidInputs)


    if format == "json":
        return mutateJSON(fileFormat, ValidInputs)
    elif format == "xml":
        return mutateXML(fileFormat,ValidInputs)
    elif format == "csv":
        return mutateCSV(fileFormat, ValidInputs)
    elif format == "jpeg":
        return mutateJPEG(fileFormat,ValidInputs)
    
        
    else:
        # return None on unable to identify file format / plaintext
        return mutator("unknown", ValidInputs)


def randMutations(corpus, maxDepth, mutClass):
    """Callable from main, start generating mutation through recursion"""

    if (maxDepth) <= 0:
        return corpus
    
    else:
        newMut = mutClass.chooseMutation(corpus)

        return randMutations(newMut, maxDepth - 1, mutClass)

# Bunch of regex to detect different formats

JSONRegex = ""


XMLRegex = ""


CSVRegex = ""


JPEGRegex = ""


