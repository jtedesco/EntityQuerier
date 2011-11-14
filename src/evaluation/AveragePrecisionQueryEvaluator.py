from src.evaluation.QueryEvaluator import QueryEvaluator

__author__ = 'jon'

class AveragePrecisionQueryEvaluator(QueryEvaluator):
    """
      Returns the average precision of a query as its score.
    """

    def __init__(self, otherPrecisions=None):
        """
          Provides a way to use this evaluator for a set of queries
        """

        QueryEvaluator.__init__(self)
        self.otherPrecisions = otherPrecisions


    def evaluate(self, results, idealResults):
        """
          Score the effectiveness of this query, using average precision
        """

        # If this is just being used for one query
        if self.otherPrecisions is None:

            # Get the average precision of this query
            results = list(results)
            idealResultSet = set(idealResults)
            numberOfRelevantResults = 0
            runningTotal = 0.0
            for i in xrange(0, len(results)):
                result = results[i]
                if result in idealResultSet:
                    numberOfRelevantResults += 1
                    runningTotal += (numberOfRelevantResults / float(i+1))

            try:
                averagePrecision = runningTotal / numberOfRelevantResults
            except ZeroDivisionError:
                averagePrecision = 0.0

        # If this is being used for all queries
        else:

            runningTotal = 0.0
            for precision in self.otherPrecisions:
                runningTotal += precision
            try:
                averagePrecision = runningTotal / len(self.otherPrecisions)
            except ZeroDivisionError:
                averagePrecision = 0.0

        return {
            'averagePrecision' : averagePrecision
        }

        
