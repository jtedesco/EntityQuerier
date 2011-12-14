from src.ranking.TermFrequencyRanking import IndexRanking
from src.ranking.scorer.BM25FBaseline import BM25FBaseline

__author__ = 'jon'

class BM25BaselineRanking(IndexRanking):
    """
      Ranking that returns the average of the Whoosh score and original Google score
    """

    def rank(self):
        reRankedResults = self.queryIndex(BM25FBaseline)
        return reRankedResults

