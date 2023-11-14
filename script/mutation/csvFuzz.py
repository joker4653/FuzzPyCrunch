import random
import string
import sys
randVals = [-1000000,-5,-4,-3,-2,-1,0,1, 2, 3, "a", "b", "c", 10000000, sys.maxsize, -sys.maxsize - 1]

# account for csv type, including headers to keep inputs somewhat reasonable
class mutateCSV:
    def __init__(self, fileformat, corpus, rows=None, columns=None) -> None:
        self.fileFormat = fileformat
        self.currentCoverage = 0
        self.lengthModifier = 1
        self.corpus = corpus # not delimited yet
    
        self.mutationFunctions = [
            self.lineOverflow, 
            self.mutateDelimeters, 
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
            self.patternBasedMutation
        ]
    


    def chooseMutation(self, corpus):
        mut = random.choice(self.mutation_functions)
        return mut(corpus)


    def emptyStr(self,corpus):
        return ''


    def removeDels(self, corpus):
        strin = corpus.split("\n")
        return "".join(strin) + "\n"


    def lineOverflow(self, corpus):
        self.lengthModifier = self.lengthModifier + 1
        return corpus * self.lengthModifier
        

    
    def addRow(self, corpus):
        # Adds a new row to the CSV
        new_row = ','.join([str(random.choice(randVals)) for i in range(corpus.count(',') // corpus.count('\n'))])
        return corpus + '\n' + new_row + '\n'



    def removeRow(self, corpus):
        # Removes a random row from the CSV
        rows = corpus.split('\n')
        if len(rows) > 1:
            rows.pop(random.randint(0, len(rows) - 1))
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return result + '\n'



    def shuffleRows(self, corpus):
        # Shuffles the rows of the CSV
        rows = corpus.split('\n')
        random.shuffle(rows)
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return result + '\n'



    def addColumn(self, corpus):
        # Adds a new column to the CSV
        rows = corpus.split('\n')
        for i in range(len(rows)):
            rows[i] += ',' + str(random.choice(randVals))
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return result + '\n'



    def removeColumn(self, corpus):
        # Removes a random column from the CSV
        rows = corpus.split('\n')[:-1]
        column_count = rows[0].count(',')
        if column_count > 0:
            col_index = random.randint(0, column_count)
            for i in range(len(rows)):
                columns = rows[i].split(',')
                columns.pop(col_index)
                rows[i] = ','.join(columns)
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return result + '\n'



    def shuffleColumns(self, corpus):
        # Shuffles the columns of the CSV


        rows = corpus.split('\n')[:-1] # final \n gives empty string, remove it

        # grab column count then indices, add 1 for final value
        columnCount = rows[0].count(',') 
        colIndices = list(range(columnCount + 1))

        random.shuffle(colIndices)

        # iterate through rows and then swap values around
        for i in range(len(rows)):
            columns = rows[i].split(',')
            rows[i] = ','.join([columns[j] for j in colIndices])

        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return result + '\n'



    def modifyHeaders(self, corpus):
        # Modifies the headers of the CSV
        rows = corpus.split('\n')
        if len(rows) > 0:
            headers = rows[0].split(',')
            for i in range(len(headers)):
                headers[i] = 'NiceHeaderBro' + str(random.choice(randVals))
            rows[0] = ','.join(headers)
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return result + '\n'



    def dataTypeMutation(self, corpus):
        # Changes the data type of random fields
        rows = corpus.split('\n')
        for i in range(1, len(rows)):
            columns = rows[i].split(',')
            for j in range(len(columns)):
                if columns[j].isdigit() and random.choice([True, False]):
                    columns[j] = str(float(columns[j])) if '.' not in columns[j] else str(int(float(columns[j])))
            rows[i] = ','.join(columns)
        result = '\n'.join(rows)
        #print(result)

        # add back final \n which caused issues earlier
        return result + '\n'



    def dataValueMutation(self, corpus):
        # Alters the values within the fields
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
        return result + '\n'



    def randomNoiseInsertion(self, corpus):
        # Adds random characters or noise into fields
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
        return result + '\n'



    def encodingErrors(self, corpus):
        # Introduces encoding errors
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
        return result + '\n'
    


    def mutateDelimeters(self, corpus):
        # Changes the delimiter of the CSV
        new_delimiter = random.choice([';', '\t', '|', '.', '\r'])  # Randomly selects a new delimiter
        new = []
        for row in corpus:
            new.append(new_delimiter.join(row))
        return str(new) + '\n'



    def integerOverflowFields(self, corpus):
        # Creates integer overflow in numeric fields
        newCorpus = ''
        for row in corpus:
            for i in range(len(row)):
                if row[i].isdigit():
                    newCorpus += str(int(row[i]) * (10**6))  # Multiplies the integer by a large number
                else:
                    newCorpus += row[i]

        #print(newCorpus)
        return newCorpus + '\n'



    def patternBasedMutation(self, corpus):
        # Introduce specific patterns like unescaped quotes, newlines in fields
        rows = corpus.split('\\n')
        for i in range(len(rows)):
            rows[i] = '\"' + rows[i].replace(',', '\"' + ',' + '\"') + '\"'
        return '\\n'.join(rows) + '\n'