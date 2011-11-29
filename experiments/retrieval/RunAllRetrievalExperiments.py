from experiments.retrieval.EntityAttributeNames import EntityAttributeNames
from experiments.retrieval.EntityAttributeNamesAndValues import EntityAttributeNamesAndValues
from experiments.retrieval.EntityAttributeValues import EntityAttributeValues
from src.queries.EntityAttributeNamesAndValuesQueryBuilder import EntityAttributeNamesAndValuesQueryBuilder
from src.queries.EntityAttributeNamesQueryBuilder import EntityAttributeNamesQueryBuilder
from src.queries.EntityAttributeValuesQueryBuilder import EntityAttributeValuesQueryBuilder
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

if __name__ == '__main__':

    numberOfSearchResults = 50
    entityIds = [
        "ChengXiang Zhai",
        "Danny Dig",
        "Kevin Chen-Chuan Chang",
        "Matthew Caesar",
        "Paris Smaragdis",
        "Ralph Johnson",
        "Robin Kravets",
    ]
    extensions = []
    searchInterface = GoogleSearch(numberOfSearchResults, True, extensions)

    for entity in entityIds:

        entityName = entity.replace(' ', '')
        entityName = entityName.replace('-', '')

        # Attribute names only
        experiment = EntityAttributeNames(entityIds, searchInterface, EntityAttributeNamesQueryBuilder(), numberOfSearchResults)
        experiment.run()
        experiment.printResults("results/%s/EntityAttributeNames" % entityName)

        # Attribute values only
        experiment = EntityAttributeValues(entityIds, searchInterface, EntityAttributeValuesQueryBuilder(), numberOfSearchResults)
        experiment.run()
        experiment.printResults("results/%s/EntityAttributeValues" % entityName)

        # Attribute names & values
        experiment = EntityAttributeNamesAndValues(entityIds, searchInterface, EntityAttributeNamesAndValuesQueryBuilder(), numberOfSearchResults)
        experiment.run()
        experiment.printResults("results/%s/EntityAttributeNamesAndValues" % entityName)