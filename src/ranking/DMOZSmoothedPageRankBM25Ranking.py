from json import load, loads
import os
import re
from src.ranking.PageRankBM25Ranking import PageRankBM25Ranking

__author__ = 'jon'

class DMOZSmoothedPageRankBM25Ranking(PageRankBM25Ranking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def __init__(self, searchResults, keywords):


        # Find where we expect this data to be cached
        self.dmozPath = str(os.getcwd())
        self.dmozPath = self.dmozPath[:self.dmozPath.find('EntityQuerier') + len('EntityQuerier')] + '/dmoz/'

        # Supplement the index with the DMOZ documents
        dmozResults = []
        for filename in os.listdir(self.dmozPath):

            # Get the contents of the file
            dmozResultData = open(self.dmozPath + filename).read()

            # Parse it out
            dmozResultData = dmozResultData.replace("\"", "\\\"")
            dmozResultData = dmozResultData.replace("'", "\"")
            dmozResultData = dmozResultData.replace("\n", " ")

            # Remove extra whitespace
            removeExtraWhitespaceRegex = re.compile(r'\s+')
            dmozResultData = re.sub(removeExtraWhitespaceRegex, ' ', dmozResultData)

            # Remove 'set' keywords
            dmozResultData = dmozResultData.replace("set([", "[")
            dmozResultData = dmozResultData.replace("])", "]")

            # Remove 'u' for unicode data
            dmozResultData = dmozResultData.replace(" u'", " '")
            dmozResultData = dmozResultData.replace(" u\"", " \"")


            dmozResult = loads(dmozResultData)
            dmozResults.append(dmozResult)

        # Create the index with both the traditional and new DMOZ search results
        searchResults.extend(dmozResults)
        super(DMOZSmoothedPageRankBM25Ranking, self).__init__(searchResults, keywords)


