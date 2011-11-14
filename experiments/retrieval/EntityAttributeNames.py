from experiments.RetrievalExperiment import RetrievalExperiment
from src.queries.EntityAttributeNamesQueryBuilder import EntityAttributeNamesQueryBuilder
from src.search.extension.PageRankExtension import PageRankExtension
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

class EntityAttributeNames(RetrievalExperiment):
    """
      A basic experiment that evaluates queries by simply assigned the score as the fraction of relevant documents retrieved
        in the first five pages of the result.
    """

if __name__ == '__main__':
    experiment = EntityAttributeNames(['Kevin Chen-Chuan Chang'], GoogleSearch(50, True, [PageRankExtension(), YQLKeywordExtension()]), EntityAttributeNamesQueryBuilder())
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeNames")
