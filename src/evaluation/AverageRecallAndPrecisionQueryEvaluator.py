from src.evaluation.PrecisionQueryEvaluator import PrecisionQueryEvaluator
from src.evaluation.QueryEvaluator import QueryEvaluator
from src.evaluation.RecallQueryEvaluator import RecallQueryEvaluator

__author__ = 'jon'

class AverageRecallAndPrecisionQueryEvaluator(QueryEvaluator):
    """
      Returns the precision of a query as its score.
    """

    def __init__(self):

        self.precisionEvaluator = PrecisionQueryEvaluator()
        self.recallEvaluator = RecallQueryEvaluator()

        
    def evaluate(self, results, idealResults):
        """
          Score the effectiveness of this query, given the results retrieved and the ideal results

            @param  results         The list of URLs retrieved
            @param  idealResults    The ideal list of URLs
        """

        # Get the recall & precision
        precision = self.precisionEvaluator.evaluate(results, idealResults)
        recall = self.recallEvaluator.evaluate(results, idealResults)
        score = (precision + recall) / 2.0
        return score
