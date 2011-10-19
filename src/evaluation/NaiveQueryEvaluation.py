from src.evaluation.QueryEvaluation import QueryEvaluation

__author__ = 'jon'

class QueryEvaluation(QueryEvaluation):
    """
      Represents the high-level interface used to evaluate the completeness of results from a query.
    """

    def evaluate(self, results, idealResults):
        """
          Score the effectiveness of this query, given the results retrieved and the ideal results

            @param  results         The results retrieved from the search engine, in the format retrieved
            @param  idealResults    The results that would be ideal, in the same format
        """

        expectedNumberOfResults = len(idealResults)
        relevantResults = set(results).intersection(set(idealResults))

        return len(relevantResults) / expectedNumberOfResults
