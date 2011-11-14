from experiments.retrieval.EntityAttributeNames import EntityAttributeNames
from experiments.retrieval.EntityAttributeNamesAndValues import EntityAttributeNamesAndValues
from experiments.retrieval.EntityAttributeValues import EntityAttributeValues
from src.queries.EntityAttributeNamesAndValuesQueryBuilder import EntityAttributeNamesAndValuesQueryBuilder
from src.queries.EntityAttributeNamesQueryBuilder import EntityAttributeNamesQueryBuilder
from src.queries.EntityAttributeValuesQueryBuilder import EntityAttributeValuesQueryBuilder
from src.search.extension.PageRankExtension import PageRankExtension
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

if __name__ == '__main__':

    numberOfSearchResults = 50
    entityIds = ['Kevin Chen-Chuan Chang']
    extensions = [
        PageRankExtension(),
        YQLKeywordExtension(),
    ]
    searchInterface = GoogleSearch(numberOfSearchResults, True, extensions)

    # Attribute names only
    experiment = EntityAttributeNames(entityIds, searchInterface, EntityAttributeNamesQueryBuilder(), numberOfSearchResults)
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeNames")

    # Attribute values only
    experiment = EntityAttributeValues(entityIds, searchInterface, EntityAttributeValuesQueryBuilder(), numberOfSearchResults)
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeValues")

    # Attribute names & values
    experiment = EntityAttributeNamesAndValues(entityIds, searchInterface, EntityAttributeNamesAndValuesQueryBuilder(), numberOfSearchResults)
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeNamesAndValues")