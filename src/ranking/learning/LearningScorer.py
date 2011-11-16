__author__ = 'jon'

from whoosh.scoring import BM25F

class LearningScorer(BM25F):
    """
      Implements a learning-based scorer for
    """

    use_final = True

    def final(self, searcher, docnum, score):
        """
          Returns the adjusted score (modified using the document's pagerank score)
        """

        pageRank = float(searcher.stored_fields(docnum)['pagerank'])
        scale = (10 + pageRank) / 10
        newScore = scale * score
        return newScore
