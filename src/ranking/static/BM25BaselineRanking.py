from src.ranking.BM25Ranking import BM25Ranking
from src.ranking.scorer import BM25FBaseline

__author__ = 'jon'

class BM25BaselineRanking(BM25Ranking):
    """
      Ranking that returns the average of the Whoosh score and original Google score
    """

    def rank(self):
        reRankedResults = self.queryIndex(BM25FBaseline)
        return reRankedResults

