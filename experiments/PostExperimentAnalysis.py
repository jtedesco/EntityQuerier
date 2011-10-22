from json import load, loads
from pprint import pprint, pformat
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


if __name__ == '__main__':

    analysis = PostExperimentAnalysis('professors/results/SimpleQueryEvaluation-SimpleQueryBuilding-KevinChang-50ResultsPerPage')
    pprint(analysis.getData())
