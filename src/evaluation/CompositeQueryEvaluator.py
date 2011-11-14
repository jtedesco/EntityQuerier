from src.evaluation.AveragePrecisionQueryEvaluator import AveragePrecisionQueryEvaluator
from src.evaluation.PrecisionQueryEvaluator import PrecisionQueryEvaluator
from src.evaluation.QueryEvaluator import QueryEvaluator
from src.evaluation.RecallQueryEvaluator import RecallQueryEvaluator

__author__ = 'jon'

class CompositeQueryEvaluator(QueryEvaluator):
    """
      Returns the precision of a query as its score.
    """

    def __init__(self, otherPrecisions=None):

        self.precisionEvaluator = PrecisionQueryEvaluator()
        self.recallEvaluator = RecallQueryEvaluator()
        self.averagePrecisionEvaluator = AveragePrecisionQueryEvaluator(otherPrecisions)

        
    def evaluate(self, results, idealResults):
        """
          Score the effectiveness of this query, given the results retrieved and the ideal results

            @param  results         The list of URLs retrieved
            @param  idealResults    The list of ideal URLs
        """

        # Get the recall, precision, and average precision
        precision = self.precisionEvaluator.evaluate(results, idealResults)
        recall = self.recallEvaluator.evaluate(results, idealResults)
        averagePrecision = self.averagePrecisionEvaluator.evaluate(results, idealResults)
        return {
            'precision' : precision['precision'],
            'recall' : recall['recall'],
            'averagePrecision' : averagePrecision['averagePrecision']
        }
