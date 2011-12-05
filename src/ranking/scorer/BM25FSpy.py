from whoosh.scoring import BM25F

class BM25FSpy(BM25F):
    """
      Collects a dictionary of the urls seen -> scores accumulated to
    """

    use_final = True

    scores = {}
    numerics = {
        'baselineScore' : {},
        'pageRank' : {}
    }

    def final(self, searcher, docnum, score):
        """
          Returns the adjusted score (modified using the document's pagerank score)
        """

        # Store the score
        url = searcher.stored_fields(docnum)['url']
        BM25FSpy.scores[url] = score
        BM25FSpy.numerics['baselineScore'][url] = searcher.stored_fields(docnum)['baselineScore']
        BM25FSpy.numerics['pageRank'][url] = searcher.stored_fields(docnum)['pagerank']
        return score
