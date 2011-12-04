from math import log
from src.search.extension.Extension import Extension

__author__ = 'jon'

class BaselineScoreExtension(Extension):

    def initialize(self, originalResults):
        """
          Initializes a baseline score extension object, given the original results retrieved from the search engine.
        """

        # A map of URL -> score
        self.scores = {}

        # Score the original results
        for query in originalResults:

            rank = 1
            numberOfResults = len(originalResults[query]['documentsRetrieved'])
            for url in originalResults[query]['documentsRetrieved']:

                rankScore = numberOfResults - rank + 1

                if url not in self.scores:
                    self.scores[url] = log(rankScore)
                else:
                    self.scores[url] = self.scores[url] + log(rankScore)

                rank += 1


    def run(self, resultDictionary):
        resultDictionary['baselineScore'] = self.scores[resultDictionary['url']]
