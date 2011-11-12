from experiments.RetrievalExperiment import RetrievalExperiment
from src.evaluation.AverageRecallAndPrecisionQueryEvaluator import AverageRecallAndPrecisionQueryEvaluator
from src.queries.EntityAttributeNamesAndValuesQueryBuilder import EntityAttributeNamesAndValuesQueryBuilder
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

class EntityAttributeNamesAndValues(RetrievalExperiment):
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
        self.searchInterface = GoogleSearch(50, True)

        # The query evaluation metric to use
        self.queryEvaluator = AverageRecallAndPrecisionQueryEvaluator()

        # The query builder for this experiment
        self.queryBuilder = EntityAttributeNamesAndValuesQueryBuilder()

        RetrievalExperiment.__init__(self, self.entityIds, self.searchInterface)


if __name__ == '__main__':
    experiment = EntityAttributeNamesAndValues()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeNamesAndValues")
