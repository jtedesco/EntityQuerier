from json import loads, load
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
        PageRankBM25Ranking.__init__(self, searchResults, keywords)