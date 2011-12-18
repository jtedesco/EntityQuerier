from experiments.RetrievalExperiment import RetrievalExperiment
from src.queries.builders.AttributeNamesAndValuesQueryBuilder import AttributeNamesAndValuesQueryBuilder
from src.queries.builders.AttributeNamesQueryBuilder import AttributeNamesQueryBuilder
from src.queries.builders.AttributeValuesQueryBuilder import AttributeValuesQueryBuilder
from src.queries.builders.order.YahooKeywordQueryBuilder import YahooKeywordQueryBuilder
from src.search.google.GoogleSearchFacade import GoogleSearchFacade


__author__ = 'jon'

if __name__ == '__main__':

    entityIds = [
        "ChengXiang Zhai",
        "Danny Dig",
        "Kevin Chen-Chuan Chang",
        "Paris Smaragdis",
        "Matthew Caesar",
        "Ralph Johnson",
        "Robin Kravets",
        "Eric Shaffer",
        "Jiawei Han",
        "Sarita Adve",

        "Papa Del's",
        "Biaggi's",
        "Chipotle",
        "Radio Maria",
        "Dos Reales",
        "Escobar's",
        "Bombay Grill",
        "Flat Top Grill",
        "Buffalo Wild Wings"
    ]


    for entityId in entityIds:

        experiments = [
            ('AttributeNames', AttributeNamesQueryBuilder, 50),
            ('AttributeValues', AttributeValuesQueryBuilder, 50),
            ('AttributeNamesAndValues', AttributeNamesAndValuesQueryBuilder, 50),
            ('YahooKeywords', YahooKeywordQueryBuilder, 50)
        ]

        for experiment in experiments:

            # Run experiment
            numberOfSearchResults = experiment[2]
            searchInterface = GoogleSearchFacade(numberOfSearchResults, True)
            retrievalExperiment = RetrievalExperiment(entityId, searchInterface, experiment[1](), numberOfSearchResults)
            retrievalExperiment.run()
            entityName = entityId.replace(' ', '').replace('-', '').replace('\'', '')
            retrievalExperiment.printResults("results/%s/%s" % (entityName, experiment[0]), entityId)
