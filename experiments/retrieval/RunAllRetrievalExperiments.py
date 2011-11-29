from experiments.RetrievalExperiment import RetrievalExperiment
from src.queries.EntityAttributeNamesAndValuesQueryBuilder import EntityAttributeNamesAndValuesQueryBuilder
from src.queries.EntityAttributeNamesQueryBuilder import EntityAttributeNamesQueryBuilder
from src.queries.EntityAttributeValuesQueryBuilder import EntityAttributeValuesQueryBuilder
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

if __name__ == '__main__':

    numberOfSearchResults = 50
    entityIds = [
#        "ChengXiang Zhai",
#        "Danny Dig",
#        "Kevin Chen-Chuan Chang",
        "Paris Smaragdis"
#        "Matthew Caesar"
#        "Ralph Johnson"
#        "Robin Kravets"
    ]
    searchInterface = GoogleSearch(numberOfSearchResults, True)

    for entity in entityIds:

        entityName = entity.replace(' ', '')
        entityName = entityName.replace('-', '')

        # Attribute names only
        experiment = RetrievalExperiment(entityIds, searchInterface, EntityAttributeNamesQueryBuilder(), numberOfSearchResults)
        experiment.run()
        experiment.printResults("results/%s/EntityAttributeNames" % entityName)

        # Attribute values only
        experiment = RetrievalExperiment(entityIds, searchInterface, EntityAttributeValuesQueryBuilder(), numberOfSearchResults)
        experiment.run()
        experiment.printResults("results/%s/EntityAttributeValues" % entityName)

        # Attribute names & values
        experiment = RetrievalExperiment(entityIds, searchInterface, EntityAttributeNamesAndValuesQueryBuilder(), numberOfSearchResults)
        experiment.run()
        experiment.printResults("results/%s/EntityAttributeNamesAndValues" % entityName)