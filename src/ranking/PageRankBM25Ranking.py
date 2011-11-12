from src.ranking.TermFrequencyRanking import TermFrequencyRanking
from src.ranking.scorer.BM25FPageRank import BM25FPageRank

__author__ = 'jon'

class PageRankBM25Ranking(TermFrequencyRanking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def getIndexLocation(self):
        indexLocation = ".index-bm25-pr"
        return indexLocation

    def rank(self):
        """
          Perform the ranking, using only the TF information from the content of the page.

            @return The reordered list of search results
        """

        reRankedResults = self.queryIndex(BM25FPageRank)
        return reRankedResults
