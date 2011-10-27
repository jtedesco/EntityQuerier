from src.evaluation.QueryEvaluator import QueryEvaluator

__author__ = 'jon'

class PrecisionQueryEvaluator(QueryEvaluator):
    """
      Returns the precision of a query as its score.
    """

    def evaluate(self, results, idealResults):
        """
          Score the effectiveness of this query, given the results retrieved and the ideal results

            @param  results         The list of URLs retrieved
            @param  idealResults    The ideal list of URLs
        """

        # Get the precision of this query
        relevantResults = set(idealResults).intersection(set(results))
        try:
            precision = len(relevantResults) / float(len(results))
        except ZeroDivisionError:
            precision = 0

        return {
            'precision' : precision
        }
