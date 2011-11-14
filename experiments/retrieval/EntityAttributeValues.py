from experiments.RetrievalExperiment import RetrievalExperiment
from src.queries.EntityAttributeValuesQueryBuilder import EntityAttributeValuesQueryBuilder
from src.search.extension.PageRankExtension import PageRankExtension
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

class EntityAttributeValues(RetrievalExperiment):
    """
      A basic experiment that evaluates queries by simply assigned the score as the fraction of relevant documents retrieved
        in the first five pages of the result.
    """


if __name__ == '__main__':
    experiment = EntityAttributeValues(['Kevin Chen-Chuan Chang'], GoogleSearch(50, True, [PageRankExtension(), YQLKeywordExtension()]), EntityAttributeValuesQueryBuilder())
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeValues")
