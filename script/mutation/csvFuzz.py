import random
import string
import sys
randVals = [-1000000,-5,-4,-3,-2,-1,0,1, 2, 3, "a", "b", "c", 10000000, sys.maxsize, -sys.maxsize - 1, -2**31,2**31-1]

class mutateCSV:
    """Class containing csv specific mutation methods"""
    def __init__(self, fileformat, corpus, rows=None, columns=None) -> None:
        self.fileFormat = fileformat
        self.currentCoverage = 0
        self.lengthModifier = 1
        self.corpus = corpus # not delimited yet
    
        self.mutationFunctions = [
            self.lineOverflow,  
            self.integerOverflowFields, 
            self.addRow, 
            self.removeRow, 
            self.shuffleRows, 
            self.addColumn, 
            self.removeColumn, 
            self.shuffleColumns, 
            self.modifyHeaders, 
            self.dataTypeMutation, 
            self.dataValueMutation, 
            self.randomNoiseInsertion, 
            self.encodingErrors,
            self.patternBasedMutation,
            self.mutateDelimeters
        ]
    


    def chooseMutation(self, corpus):
        mut = random.choice(self.mutationFunctions)
        return mut(corpus)


    def removeDels(self, corpus):
        """Remove delimeters"""
        strin = corpus.split("\n")
        return "".join(strin) + "\n"


    def lineOverflow(self, corpus):
        """Basic buffer overflow"""
        self.lengthModifier = self.lengthModifier + 1
        if self.lengthModifier > 20:
            self.lengthModifier = 0
            return corpus * self.lengthModifier

        return corpus * self.lengthModifier
        

    
    def addRow(self, corpus):
        """Add unexpected rows"""
        # Adds a new row to the CSV
        if (corpus.count('\n') != 0 or corpus.count(',') != 0):
            newRow = ','.join([str(random.choice(randVals)) for i in range(corpus.count(',') // corpus.count('\n'))])
        return str(corpus + '\n' + newRow + '\n')



    def removeRow(self, corpus):
        """Remove random rows"""
        rows = corpus.split('\n')
        if len(rows) > 1:
            rows.pop(random.randint(0, len(rows) - 1))
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return str(result + '\n')



    def shuffleRows(self, corpus):
        """Randomises row values"""
        rows = corpus.split('\n')
        random.shuffle(rows)
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return str(result + '\n')



    def addColumn(self, corpus):
        """Add extra column to input"""
        rows = corpus.split('\n')
        for i in range(len(rows)):
            rows[i] += ',' + str(random.choice(randVals))
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return str(result + '\n')



    def removeColumn(self, corpus):
        """Remove a column"""
        rows = [row for row in corpus.split('\n') if row != [] and row != '']

    
        columnCount = rows[0].count(',')
        if columnCount > 0:
            colIndex = random.randint(0, columnCount)
            for i in range(len(rows)):
                columns = rows[i].split(',')
                try:
                    columns.pop(colIndex)
                except:
                    pass

                rows[i] = ','.join(columns)
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return str(result + '\n')



    def shuffleColumns(self, corpus):
        """Shuffles the columns around"""


        rows = [row for row in corpus.split('\n') if row != [] and row != ''] # final \n gives empty string, remove it

        # grab column count then indices, add 1 for final value
        columnCount = rows[0].count(',') 
        colIndices = list(range(columnCount + 1))

        random.shuffle(colIndices)

        # iterate through rows and then swap values around
        for i in range(len(rows)):
            columns = rows[i].split(',')

            try:
                rows[i] = ','.join([columns[j] for j in colIndices])
            except:
                pass

        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return str(result + '\n')



    def modifyHeaders(self, corpus):
        """Cook the headers"""
        rows = corpus.split('\n')
        if len(rows) > 0:
            headers = rows[0].split(',')
            for i in range(len(headers)):
                headers[i] = 'NiceHeaderBro' + str(random.choice(randVals))
            rows[0] = ','.join(headers)
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return str(result + '\n')



    def dataTypeMutation(self, corpus):
        """change data types in rnadom fields"""
        rows = corpus.split('\n')
        for i in range(1, len(rows)):
            columns = rows[i].split(',')
            for j in range(len(columns)):
                """Check if digit for error sakes"""
                if columns[j].isdigit() and random.choice([True, False]):
                    columns[j] = str(float(columns[j])) if '.' not in columns[j] else str(int(float(columns[j])))
            rows[i] = ','.join(columns)
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return str(result + '\n')



    def dataValueMutation(self, corpus):
        """Just change random vals"""
        rows = corpus.split('\n')
        for i in range(1, len(rows)):
            columns = rows[i].split(',')
            for j in range(len(columns)):
                if random.choice([True, False]):
                    columns[j] = str(random.choice(randVals))
            rows[i] = ','.join(columns)
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return str(result + '\n')



    def randomNoiseInsertion(self, corpus):
        """Add random noise into the inputs"""
        rows = corpus.split('\n')
        for i in range(1, len(rows)):
            columns = rows[i].split(',')
            for j in range(len(columns)):
                if random.choice([True, False]):
                    columns[j] += random.choice(string.ascii_letters)
            rows[i] = ','.join(columns)
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return str(result + '\n')



    def encodingErrors(self, corpus):
        """break the encoding see if there is a parsing error"""
        rows = corpus.split('\n')
        for i in range(1, len(rows)):
            columns = rows[i].split(',')
            for j in range(len(columns)):
                if random.choice([True, False]):
                    columns[j] = columns[j].encode('ascii', 'replace').decode('ascii')
            rows[i] = ','.join(columns)
        result = '\n'.join(rows)
        #print(result)
        
        # add back final \n which caused issues earlier
        return str(result + '\n')
    


    def mutateDelimeters(self, corpus):
        """Change the delims up"""
        newDelimiter = random.choice([';', '\t', '|', '.', '\r'])  # Randomly selects a new delimiter
        new = []
        for row in corpus:
            new.append(newDelimiter.join(row))
        return str(new) + '\n'



    def integerOverflowFields(self, corpus):
        """Force integer overflow"""
        newCorpus = ''
        for row in corpus:
            for i in range(len(row)):
                if row[i].isdigit():
                    newCorpus += str(int(sys.maxsize))  # Multiplies the integer by a large number
                else:
                    newCorpus += row[i]

        #print(newCorpus)
        return str(newCorpus + '\n')



    def patternBasedMutation(self, corpus):
        """Bring in command characters and escape characters"""
        rows = corpus.split('\\n')
        for i in range(len(rows)):
            if (random.choice([True,False])):
                rows[i] = '\"' + rows[i].replace(',', '\"' + ',' + '\"') + '\"'
        return str('\\n'.join(rows) + '\n')