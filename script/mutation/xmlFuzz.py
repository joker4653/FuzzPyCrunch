import random
import copy
import string
import re
import xml.etree.ElementTree as ET
import sys
class mutateXML:
    def __init__(self, fileFormat, corpus):
        self.fileFormat = fileFormat
        self.currentCoverage = 0
        self.lengthModifier = 1
        self.corpus = corpus
        self.root = ET.parse(sys.argv[2])

        self.mutationFunctions = [
            self.insertRandomNodes,
            self.removeRandomAttributes,
            self.changeTagNames,
            self.invertNodeOrder,
            self.replaceTextContent,
            self.randomEncoding,
            self.changeCommentStructure,
        ]


    def chooseMutation(self, corpus):
        mut = random.choice(self.mutationFunctions)
        return mut(corpus)


    def randomEncoding(self, corpus):
        """Randomly encode/escape characters in the XML"""
        replacements =  ['"', '&quot;', '\'', '&apos;', '<', '&lt;', '>', '&gt;', '&', '&amp']
        for char, escape in replacements.items():
            corpus = corpus.replace(char, escape)
        return corpus



    def changeCommentStructure(self, corpus):
        """ Change the structure of comments in the XML"""
        # For changing comment structure, we will randomly wrap texts with comment tags
        texts = re.findall('>([^<]+)<', corpus)
        for text in texts:
            if random.choice([True, False]):
                corpus = corpus.replace('>' + text + '<', '><!-- ' + text.strip() + ' --><')
        return corpus



    def invertNodeOrder(self, corpus):
        """Invert the order of nodes in the XML"""
        try:
            root = ET.fromstring(corpus)
            for parent in root.iter():
                parent[:] = parent[::-1]
            return ET.tostring(root, encoding='unicode')
        except ET.ParseError:
            return corpus



    def replaceTextContent(self, corpus):
        """Replace the text content of nodes randomly in the XML"""
        try:
            root = ET.fromstring(corpus)
            for elem in root.iter():
                if elem.text:
                    elem.text = ''.join(random.choices(string.ascii_letters, k=10))
            return ET.tostring(root, encoding='unicode')
        except ET.ParseError:
            return corpus


    def removeRandomAttributes(self, corpus):
        """Remove random attributes from nodes in the XML"""
        try:
            root = ET.fromstring(corpus)
            for elem in root.iter():
                if elem.attrib:
                    attr_to_remove = random.choice(list(elem.attrib.keys()))
                    del elem.attrib[attr_to_remove]
            return ET.tostring(root, encoding='unicode')
        except ET.ParseError:
            return corpus



    def changeTagNames(self, corpus):
        """Change the names of tags randomly in the XML"""
        try:
            root = ET.fromstring(corpus)
            for elem in root.iter():
                elem.tag = 'changed_' + elem.tag
            return ET.tostring(root, encoding='unicode')
        except ET.ParseError:
            return corpus




    def insertRandomNodes(self, corpus):
        """Insert random nodes into the XML"""
        try:
            root = ET.fromstring(corpus)
            for _ in range(random.randint(1, 3)):
                random_node = ET.Element('randomNode')
                random_node.text = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
                root.insert(random.randint(0, len(root)), random_node)
            return ET.tostring(root, encoding='unicode')
        except ET.ParseError:
            return corpus
    