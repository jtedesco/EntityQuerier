from experiments.RetrievalExperiment import RetrievalExperiment
from src.queries.EntityAttributeNamesAndValuesQueryBuilder import EntityAttributeNamesAndValuesQueryBuilder
from src.search.extension.PageRankExtension import PageRankExtension
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

class EntityAttributeNamesAndValues(RetrievalExperiment):
    """
      A basic experiment that evaluates queries by simply assigned the score as the fraction of relevant documents retrieved
        in the first five pages of the result.
    """

if __name__ == '__main__':
    experiment = EntityAttributeNamesAndValues(['Kevin Chen-Chuan Chang'], GoogleSearch(50, True, [PageRankExtension(), YQLKeywordExtension()]), EntityAttributeNamesAndValuesQueryBuilder())
    experiment.run()
    experiment.printResults("results/KevinChenChuanChang-EntityAttributeNamesAndValues")
