from json import load
import os
from src.ranking.BM25Ranking import BM25Ranking

__author__ = 'jon'

class DMOZSmoothed1000BM25Ranking(BM25Ranking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def __init__(self, searchResults, keywords, dmozResultsToUse=1000):


        # Find where we expect this data to be cached
        self.dmozPath = str(os.getcwd())
        self.dmozPath = self.dmozPath[:self.dmozPath.find('EntityQuerier') + len('EntityQuerier')] + '/dmoz/'

        # Supplement the index with the DMOZ documents
        dmozResults = []
        count = 0
        for filename in os.listdir(self.dmozPath):

            count += 1

            if count < dmozResultsToUse:
                
                try:

                    # Get the contents of the file
                    dmozResultFile = open(self.dmozPath + filename)
                    dmozResult = load(dmozResultFile)
                    dmozResults.append(dmozResult)

                except ValueError:

                    # Do something awful...
                    try:
                        dmozResult = eval(dmozResultFile.read())
                        dmozResults.append(dmozResult)
                    except Exception:
                        pass

        # Create the index with both the traditional and new DMOZ search results
        searchResults.extend(dmozResults)
        self.indexLocation = ".dmoz-1000-index"
        BM25Ranking.__init__(self, searchResults, keywords)

    @staticmethod
    def getIndexLocation():
        return ".dmoz-1000-index"