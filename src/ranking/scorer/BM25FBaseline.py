from whoosh.scoring import BM25F

class BM25FBaseline(BM25F):
    """
      Implements the BM25F scoring algorithm.
    """

    use_final = True

    def final(self, searcher, docnum, score):
        """
          Returns the adjusted score (modified using the document's pagerank score)
        """

        baselineScore = float(searcher.stored_fields(docnum)['baselineScore'])
        averageScore = (baselineScore + score) / 2.0
        return averageScore
