from whoosh import scoring
from src.ranking.IndexRanking import IndexRanking

__author__ = 'jon'

class BM25Ranking(IndexRanking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def rank(self):
        """
          Perform the ranking, using only the TF information from the content of the page.

            @return The reordered list of search results
        """

        reRankedResults = self.queryIndex(scoring.BM25F)
        return reRankedResults
