from whoosh.scoring import BM25F

class BM25FPageRank(BM25F):
    """
      Implements the BM25F scoring algorithm.
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
