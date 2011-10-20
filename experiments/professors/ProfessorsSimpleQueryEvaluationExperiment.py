from experiments.Experiment import Experiment
from src.evaluation.SimpleQueryEvaluator import SimpleQueryEvaluator
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

class ProfessorsSimpleQueryEvaluationExperiment(Experiment):
    """
      A basic experiment that evaluates queries by simply assigned the score as the fraction of relevant documents retrieved
        in the first five pages of the result.
    """

    def __init__(self):
        """
          Initialize this experiment's data.
        """

        # The list of ids (corresponding JSON files are expected to be found in 'standard' and 'entities' folders)
        entityIds = [
            'ChengXiang Zhai',
            'Paris Smaragdis',
            'Robin Kravets',
            'Matthew Caesar',
            'Kevin Chen-Chuan Chang',
            'Danny Dig',
            'Ralph Johnson'
        ]

        # The search engine to use
        searchInterface = GoogleSearch()

        # The query evaluation metric to use
        self.queryEvaluator = SimpleQueryEvaluator()

        Experiment.__init__(self, entityIds, searchInterface)
