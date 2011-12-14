from src.ranking.TermFrequencyRanking import IndexRanking
from src.ranking.scorer.BM25FPageRank import BM25FPageRank

__author__ = 'jon'

class BM25PageRankRanking(IndexRanking):
    """
      Ranking that returns the original score scaled by PR
    """

    def rank(self):
        reRankedResults = self.queryIndex(BM25FPageRank)
        return reRankedResults