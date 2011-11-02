from experiments.RetrievalExperiment import RetrievalExperiment
from src.evaluation.AverageRecallAndPrecisionQueryEvaluator import AverageRecallAndPrecisionQueryEvaluator
from src.queries.EntityAttributeNamesValuesQueryAndOperatorsBuilder import EntityAttributeNamesValuesQueryAndOperatorsBuilder
from src.search.google.GoogleSearch import GoogleSearch
from src.search.wrappers.FollowLinksSearch import FollowLinksSearch
from src.search.wrappers.TopKKeywordSearch import TopKKeywordSearch

__author__ = 'jon'

class EntityAttributeNamesValuesOperatorsFollowingLinksAndKeywords(RetrievalExperiment):
    """
      A basic experiment that evaluates queries by simply assigned the score as the fraction of relevant documents retrieved
        in the first five pages of the result.
    """

    def __init__(self):
        """
          Initialize this experiment's data.
        """

        # The list of ids (corresponding JSON files are expected to be found in 'standard' and 'entities' folders)
        self.entityIds = [
            'Kevin Chen-Chuan Chang'
        ]

        # The search engine to use
        k = 10
        resultsToRetrieve = 50
        self.searchInterface = FollowLinksSearch(TopKKeywordSearch(GoogleSearch(resultsToRetrieve, True), resultsToRetrieve, True, 10), resultsToRetrieve, True, k)

        # The query evaluation metric to use
        self.queryEvaluator = AverageRecallAndPrecisionQueryEvaluator()

        # The query builder for this experiment
        self.queryBuilder = EntityAttributeNamesValuesQueryAndOperatorsBuilder()

        RetrievalExperiment.__init__(self, self.entityIds, self.searchInterface)


if __name__ == '__main__':
    experiment = EntityAttributeNamesValuesOperatorsFollowingLinksAndKeywords()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeNamesValuesOperatorsFollowingLinksAndKeywords")
