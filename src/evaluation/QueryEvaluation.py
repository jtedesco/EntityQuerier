__author__ = 'jon'

class QueryEvaluation(object):
    """
      Represents the high-level interface used to evaluate the completeness of results from a query.
    """

    def __init__(self, query):
        self.query = query


    def evaluate(self, results, idealResults):
        """
          Score the effectiveness of this query, given the results retrieved and the ideal results

            @param  results         The results retrieved from the search engine, in the format retrieved
            @param  idealResults    The results that would be ideal, in the same format
        """

        raise NotImplementedError()



        
