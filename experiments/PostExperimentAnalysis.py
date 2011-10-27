from json import load, loads
from pprint import pprint, pformat
from PostExperimentQueryScorer import recallQueryScore, precisionQueryScore, combinedRecallAndPrecisionQueryScore
import re

__author__ = 'jon'

class PostExperimentAnalysis(object):
    """
      Allows us to analyze the results and information about a set of results.
    """

    def __init__(self, resultsFilePath):
        """
          Parses out the data from the results file.
        """

        # Get the contents of the file
        resultsData = open(resultsFilePath).read()

        # Parse it out
        resultsData = resultsData.replace("\"", "\\\"")
        resultsData = resultsData.replace("'", "\"")
        resultsData = resultsData.replace("\n", " ")

        # Remove extra whitespace
        removeExtraWhitespaceRegex = re.compile(r'\s+')
        resultsData = re.sub(removeExtraWhitespaceRegex, ' ', resultsData)

        # Remove 'set' keywords
        resultsData = resultsData.replace("set([", "[")
        resultsData = resultsData.replace("])", "]")

        # Load the data
        self.resultsData = loads(resultsData)


    def getData(self):
        """
          Print out the precision & recall for each query, and overall.
        """

        data = {}
        for entityId in self.resultsData:

            entityId = str(entityId)
            data[entityId] = {}

            for query in self.resultsData[entityId]:

                query = str(query)
                data[entityId][query] = {}

                try:

                    # Get the precision and recall for this
                    precision = len(self.resultsData[entityId][query]['relevantDocumentsRetrieved']) \
                            / float(len(self.resultsData[entityId][query]['documentsRetrieved']))

                except ZeroDivisionError:

                    precision = 0

                # Calculate the recall
                recall = len(self.resultsData[entityId][query]['relevantDocumentsRetrieved']) / \
                         float(len(self.resultsData[entityId][query]['relevantDocumentsNotRetrieved'])
                         + len(self.resultsData[entityId][query]['relevantDocumentsRetrieved']))


                data[entityId][query]['precision'] = precision
                data[entityId][query]['recall'] = recall

        return data


    def getQueryScoreBasedOrdering(self, scoreFunction):
        """
          Performs a greedy sorting algorithm (based on the score of queries as determined by the
            function parameter) on the queries submitted to see what order would be ideal using
            this set of queries.

            @param  scoreFunction   The function to use for scoring a query
        """

        data = {}
        for entityId in self.resultsData:

            # Remove the 'overall' from the list of queries for this entity
            overallData = self.resultsData[entityId]['overall']
            del self.resultsData[entityId]['overall']
            stupidQuery = '"' + str(entityId) + '" "' + str(entityId) + '"'
            if stupidQuery in self.resultsData[entityId].keys():
                del self.resultsData[entityId][stupidQuery]

            # Get the total number of relevant results
            totalRelevantDocumentsRetrieved = overallData['relevantDocumentsRetrieved']
            totalRelevantDocumentsNotRetrieved  = overallData['relevantDocumentsRetrieved']
            numberOfRelevantResults = len(totalRelevantDocumentsRetrieved) + len(totalRelevantDocumentsNotRetrieved)

            # Holds the total set of results retrieved at any point in time through the iterations (as a set of URLs)
            resultsRetrieved = set([])
            relevantResultsRetrieved = set([])
            queriesNotUsed = list(self.resultsData[entityId].keys())

            # The data structures for performing this simulation
            queries = []
            precisions = []
            scores = []
            recalls = []

            # Iterate through all of the queries
            numberOfQueries = len(self.resultsData[entityId])
            for i in xrange(0, numberOfQueries):

                # Score the queries by the number of new relevant documents that will be retrieved
                #   indexed by query, value is the score (the new recall once this query is performed)
                queryScores = {}
                for query in queriesNotUsed:

                    # Get the relevant results, new relevant results, duplicate relevant results, and nonrelevant results for this query
                    relevantResults = set(self.resultsData[entityId][query]['relevantDocumentsRetrieved'])
                    newRelevantResults = set(relevantResults).difference(set(relevantResultsRetrieved))
                    duplicateRelevantResults = relevantResults.difference(newRelevantResults)
                    nonRelevantNewResults = self.resultsData[entityId][query]['nonRelevantDocumentsRetrieved']

                    queryScore = scoreFunction(newRelevantResults, duplicateRelevantResults, nonRelevantNewResults, relevantResultsRetrieved,
                                               resultsRetrieved, totalRelevantDocumentsRetrieved, totalRelevantDocumentsNotRetrieved)
                    queryScores[query] = queryScore

                # Find the highest scoring query for this iteration
                highestScore = 0
                highestQuery = None
                for query in queryScores:
                    if queryScores[query] > highestScore:
                        highestScore = queryScores[query]
                        highestQuery = query

                # Update the results so far
                if highestQuery is not None:

                    # Update the series of queries and the scores
                    queries.append(str(highestQuery))
                    scores.append(highestScore)

                    # Get the relevant results, new relevant results, duplicate relevant results, and nonrelevant results for this query
                    relevantResults = set(self.resultsData[entityId][highestQuery]['relevantDocumentsRetrieved'])
                    newRelevantResults = set(relevantResults).difference(set(relevantResultsRetrieved))
                    duplicateRelevantResults = relevantResults.difference(newRelevantResults)
                    nonRelevantNewResults = self.resultsData[entityId][highestQuery]['nonRelevantDocumentsRetrieved']

                    # Find recall & update list of recalls
                    queryRecall = recallQueryScore(newRelevantResults, duplicateRelevantResults, nonRelevantNewResults, relevantResultsRetrieved,
                                               resultsRetrieved, totalRelevantDocumentsRetrieved, totalRelevantDocumentsNotRetrieved)
                    recalls.append(queryRecall)

                    # Find precision & update list of precisions
                    queryPrecision = precisionQueryScore(newRelevantResults, duplicateRelevantResults, nonRelevantNewResults, relevantResultsRetrieved,
                                               resultsRetrieved, totalRelevantDocumentsRetrieved, totalRelevantDocumentsNotRetrieved)
                    precisions.append(queryPrecision)

                    # Remove this query from 'queriesNotUsed', it has been analyzed now
                    queriesNotUsed.remove(highestQuery)

            # Holds the information for series of queries
            #   'queries' is the list queries, in order, that would be ideal
            #   'precisions' is the list of precisions, corresponding to each stage of the retrival process
            #   'recalls' is the list of recall values at each stage of the retrieval process
            data[entityId] = {
                'queries': queries,
                'precisions': precisions,
                'recalls': recalls,
                'scores': scores
            }

            self.resultsData[entityId]['overall'] = overallData

            return data


    def printAnalysisResults(self, analysisResults):
        """
          Prints the analysis results in a table

            @param  analysisResults    The analysis to print out as a table
        """

        for entityId in analysisResults:

            numberOfQueries = len(analysisResults[entityId][analysisResults[entityId].keys()[0]])

            # Iterate through rows of the table & print it out, formatted nicely
            a = 15
            b = 75
            print repr("Query").rjust(b), repr("Score").center(a), repr("Recall").center(a), repr("Precision").center(a)
            print repr('='*(b-5)).rjust(b), repr('='*(a-5)).center(a), repr('='*(a-5)).center(a), repr('='*(a-5)).center(a)
            for i in xrange(0, numberOfQueries):
                query = analysisResults[entityId]['queries'][i]
                recall = analysisResults[entityId]['recalls'][i]
                precision = analysisResults[entityId]['precisions'][i]
                score = analysisResults[entityId]['scores'][i]
                print repr(query).rjust(b), repr('{0:.3f}'.format(score)).center(a), repr('{0:.3f}'.format(recall)).center(a), repr('{0:.3f}'.format(precision)).center(a)



if __name__ == '__main__':

    analysis = PostExperimentAnalysis('professors/results/SimpleQueryEvaluation-SimpleQueryBuilding-KevinChang-50ResultsPerPage')
    print "Results-based scoring:"
    analysis.printAnalysisResults(analysis.getQueryScoreBasedOrdering(combinedRecallAndPrecisionQueryScore))
#    print "\nPrecision-based scoring"
#    pprint(analysis.getQueryScoreBasedOrdering(precisionQueryScore))
#    print "\nRecall & precision scoring"
#    pprint(analysis.getQueryScoreBasedOrdering(combinedRecallAndPrecisionQueryScore))
