from whoosh import scoring
from src.ranking.TermFrequencyRanking import TermFrequencyRanking

__author__ = 'jon'

class PL2Ranking(TermFrequencyRanking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def getIndexLocation(self):
        indexLocation = ".index-pl2"
        return indexLocation


    def rank(self):
        """
          Perform the ranking, using the PL2 algorithm

            @return The reordered list of search results
        """

        reRankedResults = self.queryIndex(scoring.PL2)
        return reRankedResults
