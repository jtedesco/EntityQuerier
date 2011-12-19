from json import  loads, load
import os
import sys

__author__ = 'jon'

alphabet = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}


def splitCamelCase(camelCaseString):
    """
      Splits camel case string into separate words
    """

    outputBuffer = ""
    camelCaseString = camelCaseString[0].upper() + camelCaseString[1:]
    for index in xrange(0,len(camelCaseString)-1):
        character = camelCaseString[index]
        nextCharacter = camelCaseString[index+1]

        if character == character.upper() and nextCharacter == nextCharacter.lower():
            outputBuffer += ' ' + character
        else:
            outputBuffer += character

        if index+1 == len(camelCaseString) - 1:
            outputBuffer += nextCharacter

    if outputBuffer[-1] not in alphabet and outputBuffer[-2] in alphabet:
        outputBuffer = outputBuffer[:-1] + ' ' + outputBuffer[-1]

    return outputBuffer.strip()


def parseStatsFromRanking(rankingFile):

    content = open(rankingFile).read().split('\n')

    # Get precisions and average precisions
    for i in xrange(1, 5):
        contentLine = content[i]


        firstColon = contentLine.find(':')
        divider = contentLine.find('|')
        lastColon = contentLine.rfind(':')

        precision = float(contentLine[firstColon+1:divider-1].strip())
        averagePrecision = float(contentLine[lastColon+1:].strip())

        if i == 1:
            precisionAt1 = precision
            averagePrecisionAt1 = averagePrecision
        elif i == 2:
            precisionAt10 = precision
            averagePrecisionAt10 = averagePrecision
        elif i == 3:
            precisionAt20 = precision
            averagePrecisionAt20 = averagePrecision
        elif i == 4:
            precisionAt50 = precision
            averagePrecisionAt50 = averagePrecision

    # Split line with recall at 50, r-precision, and precision at 100 % recall
    dataBits = content[6].split(' | ')
    recallAt50 = float(dataBits[0][dataBits[0].find(':')+1:].strip())
    rPrecision = float(dataBits[1][dataBits[1].find(':')+1:].strip())
    fullPrecision = float(dataBits[2][dataBits[2].find(':')+1:].strip())

    return precisionAt1, precisionAt10, precisionAt20, precisionAt50, averagePrecisionAt1, averagePrecisionAt10, \
                    averagePrecisionAt20,  averagePrecisionAt50, recallAt50, rPrecision, fullPrecision


def averageEntityScores(data):

    # Get the experiments and metrics stored for each entity
    entities = data.keys()
    experiments = data[entities[0]].keys()
    metrics = data[entities[0]][experiments[0]].keys()

    averagedData = {}
    for experiment in experiments:
        averagedData[experiment] = {}
        for metric in metrics:

            average = 0.0
            numberOfEntities = len(entities)
            for entity in entities:
                try:
                    average += data[entity][experiment][metric]
                except KeyError:
                    numberOfEntities -= 1
                    print "Skipping %s for experiment '%s'" % (entity, experiment)
            average /= numberOfEntities

            averagedData[experiment][metric] = average

    return averagedData


def populateRankingData(data, rootDirectory):
    
    for folder in os.listdir(rootDirectory):
        entityName = folder
        entityDirectory = rootDirectory + '/' + folder

        data[entityName] = {}

        if os.path.isdir(entityDirectory):
            for experimentFile in os.listdir(entityDirectory):
                experimentName = experimentFile

                experimentPath = entityDirectory + '/' + experimentFile
                if os.path.isfile(experimentPath):

                    # Parse the data from the ranking output
                    precisionAt1, precisionAt10, precisionAt20, precisionAt50, averagePrecisionAt1, averagePrecisionAt10,\
                    averagePrecisionAt20, averagePrecisionAt50, recallAt50, rPrecision, fullPrecision = parseStatsFromRanking(
                        experimentPath)
    
                    # Insert all these data points
                    data[entityName][experimentName] = {
                        'precisionAt10': precisionAt10,
                        'precisionAt20': precisionAt20,
                        'precisionAt50': precisionAt50,
                        'averagePrecisionAt1': averagePrecisionAt1,
                        'averagePrecisionAt10': averagePrecisionAt10,
                        'averagePrecisionAt20': averagePrecisionAt20,
                        'averagePrecisionAt50': averagePrecisionAt50,
                        'recallAt50': recallAt50,
                        'rPrecision': rPrecision,
                        'fullPrecision': fullPrecision
                    }


def parseStatsFromRetrieval(retrievalFile):

    content = open(retrievalFile).read().split('\n')

    # Get the text lines containing stats
    recallLine = content[5]
    averagePrecisionLine = content[6]
    precisionLine = content[7]

    # Reconstruct the query results
    queries = loads('\n'.join(content[10:]))
    numberOfQueries = len(queries.keys())
    
    # Get the actual numbers
    recall = float(recallLine[recallLine.find(':')+1:].strip())
    averagePrecision = float(averagePrecisionLine[averagePrecisionLine.find(':')+1:].strip())
    precision = float(precisionLine[precisionLine.find(':')+1:].strip())

    return recall, averagePrecision, precision, numberOfQueries


def populateRetrievalData(data, rootDirectory):

    for folder in os.listdir(rootDirectory):
        entityName = folder
        entityDirectory = rootDirectory + '/' + folder

        data[entityName] = {}

        if os.path.isdir(entityDirectory):
            for experimentFile in os.listdir(entityDirectory):
                experimentName = experimentFile

                experimentPath = entityDirectory + '/' + experimentFile
                if os.path.isfile(experimentPath):

                    recall, averagePrecision, precision, numberOfQueries = parseStatsFromRetrieval(experimentPath)

                    data[entityName][experimentName] = {
                        'precision' : precision,
                        'recall' : recall,
                        'averagePrecision' : averagePrecision,
                        'numberOfQueries' : numberOfQueries
                    }

def getHumanAverageScores(rootDirectory):
    """
      Gets the average scores for human queries
    """

    # Get the average number of queries required by the human baseline
    averageNumberOfQueries = 0.0
    entityIds = os.listdir(rootDirectory + '/entities/efficiencyStandard')
    for entityId in entityIds:
        try:
            queries = load(open(rootDirectory + '/entities/efficiencyStandard/' + entityId))
        except:
            print "Error with '%s': '%s" % (entityId, str(sys.exc_info()[1]))
            sys.exit()
        averageNumberOfQueries += len(queries)
    averageNumberOfQueries /= len(entityIds)

    averageScores = {
        'precision' : 1.0,
        'recall' : 1.0,
        'numberOfQueries' : averageNumberOfQueries
    }

    return averageScores




    