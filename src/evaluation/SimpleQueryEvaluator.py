from src.evaluation.QueryEvaluator import QueryEvaluator

__author__ = 'jon'

class SimpleQueryEvaluator(QueryEvaluator):
    """
      Represents the high-level interface used to evaluate the completeness of results from a query.
    """

    def evaluate(self, results, idealResults):
        """
          Score the effectiveness of this query, given the results retrieved and the ideal results

            @param  results         The list of URLs retrieved
            @param  idealResults    The ideal list of URLs
        """

        expectedNumberOfResults = len(idealResults)
        relevantResults = set(idealResults).intersection(set(results))
        return len(relevantResults) / float(expectedNumberOfResults)
