from src.evaluation.QueryEvaluator import QueryEvaluator

__author__ = 'jon'

class RecallQueryEvaluator(QueryEvaluator):
    """
      Returns the recall of a query as its score
    """

    def evaluate(self, results, idealResults):
        """
          Score the effectiveness of this query, given the results retrieved and the ideal results

            @param  results         The list of URLs retrieved
            @param  idealResults    The ideal list of URLs
        """

        expectedNumberOfResults = len(idealResults)
        relevantResults = set(idealResults).intersection(set(results))

        try:
            recall = len(relevantResults) / float(expectedNumberOfResults)
        except ZeroDivisionError:
            recall = 0
            
        return {
            'recall' : recall
        }
