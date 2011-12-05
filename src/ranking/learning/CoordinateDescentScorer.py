__author__ = 'jon'

from whoosh.scoring import BM25F

class CoordinateDescentScorer(BM25F):
    """
      Implements a learning-based scorer for
    """

    use_final = True
    pageRankScalingWeight = 1.0
    pageRankWeight = 1.0
    baselineScoreWeight = 1.0

    def final(self, searcher, docnum, score):
        """
          Returns the adjusted score (modified using the document's pagerank score)
        """

        # Add the raw weight & scaling from pagerank
        pageRank = float(searcher.stored_fields(docnum)['pagerank'])
        baselineScore = float(searcher.stored_fields(docnum)['baselineScore'])
        newScore = CoordinateDescentScorer.pageRankScalingWeight * ((CoordinateDescentScorer.baselineScoreWeight * baselineScore) + score + (pageRank * CoordinateDescentScorer.pageRankWeight))

        return newScore
