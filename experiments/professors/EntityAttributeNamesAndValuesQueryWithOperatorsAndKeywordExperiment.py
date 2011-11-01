from pprint import pprint
from experiments.Experiment import Experiment
from experiments.PostExperimentAnalysis import PostExperimentAnalysis
from src.analysis.TermFrequencyAnalysis import TermFrequencyAnalysis
from src.evaluation.AverageRecallAndPrecisionQueryEvaluator import AverageRecallAndPrecisionQueryEvaluator
from src.queries.EntityAttributeNamesAndValuesQueryWithOperatorsBuilder import EntityAttributeNamesAndValuesQueryWithOperatorsBuilder
from src.search.google.GoogleSearch import GoogleSearch
from src.search.wrappers.TopKKeywordSearch import TopKKeywordSearch
from json import loads
from util.GoogleResultsBuilder import buildGoogleResultsFromURLs

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
        self.searchInterface = TopKKeywordSearch(GoogleSearch(50, True), 50, True, 10)

        # The query evaluation metric to use
        self.queryEvaluator = AverageRecallAndPrecisionQueryEvaluator()

        # The query builder for this experiment
        self.queryBuilder = EntityAttributeNamesAndValuesQueryWithOperatorsBuilder()

        Experiment.__init__(self, self.entityIds, self.searchInterface)


if __name__ == '__main__':

    analysis = PostExperimentAnalysis("results/KevinChang-EntityNamesAndValues")
    results = analysis.resultsData
    for entityId in results:

        urls = []
        for category in results[entityId]:
            for query in results[entityId][category]:
                for url in results[entityId][category][query]:
                    if 'http' in url:
                        urls.append(url)
        searchResults = buildGoogleResultsFromURLs(urls)

        termFrequencyAnalysis = TermFrequencyAnalysis(searchResults)
        topWords = termFrequencyAnalysis.getTopKWords(10)
        pprint(topWords)


#    experiment = EntityAttributeNamesAndValuesQueryWithOperatorsAndKeywordExperiment()
#    experiment.run()
#    experiment.printResults("results/KevinChang-EntityNamesAndValuesWithOperatorsAndKeywords")
