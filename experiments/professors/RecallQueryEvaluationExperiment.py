from experiments.Experiment import Experiment
from src.evaluation.SimpleQueryEvaluator import RecallQueryEvaluator
from src.queries.builder.SimpleQueryBuilder import SimpleQueryBuilder
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

class RecallQueryEvaluationExperiment(Experiment):
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
        self.searchInterface = GoogleSearch()

        # The query evaluation metric to use
        self.queryEvaluator = RecallQueryEvaluator()

        # The query builder for this experiment
        self.queryBuilder = SimpleQueryBuilder()

        Experiment.__init__(self, self.entityIds, self.searchInterface)


if __name__ == '__main__':
    experiment = RecallQueryEvaluationExperiment()
    experiment.run()
    experiment.printResults()
