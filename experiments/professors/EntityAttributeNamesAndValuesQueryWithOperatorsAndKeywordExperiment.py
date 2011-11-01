from pprint import pprint
from experiments.Experiment import Experiment
from src.analysis.TermFrequencyAnalysis import TermFrequencyAnalysis
from src.evaluation.AverageRecallAndPrecisionQueryEvaluator import AverageRecallAndPrecisionQueryEvaluator
from src.queries.EntityAttributeNamesAndValuesQueryWithOperatorsBuilder import EntityAttributeNamesAndValuesQueryWithOperatorsBuilder
from src.search.google.GoogleSearch import GoogleSearch
from src.search.wrappers.TopKKeywordSearch import TopKKeywordSearch

__author__ = 'jon'

class EntityAttributeNamesAndValuesQueryWithOperatorsAndKeywordExperiment(Experiment):
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
        resultsToRetrieve = 10
        self.searchInterface = TopKKeywordSearch(GoogleSearch(resultsToRetrieve, True), resultsToRetrieve, True, 10)

        # The query evaluation metric to use
        self.queryEvaluator = AverageRecallAndPrecisionQueryEvaluator()

        # The query builder for this experiment
        self.queryBuilder = EntityAttributeNamesAndValuesQueryWithOperatorsBuilder()

        Experiment.__init__(self, self.entityIds, self.searchInterface)


if __name__ == '__main__':
    experiment = EntityAttributeNamesAndValuesQueryWithOperatorsAndKeywordExperiment()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityNamesAndValuesWithOperatorsAndKeywords")