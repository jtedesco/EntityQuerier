from whoosh import scoring
from src.ranking.TermFrequencyRanking import TermFrequencyRanking

__author__ = 'jon'

class BM25Ranking(TermFrequencyRanking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def getIndexLocation(self):
        indexLocation = ".index-bm25"
        return indexLocation


    def rank(self):
        """
          Perform the ranking, using only the TF information from the content of the page.

            @return The reordered list of search results
        """

        reRankedResults = self.queryIndex(scoring.BM25F)
        return reRankedResults
