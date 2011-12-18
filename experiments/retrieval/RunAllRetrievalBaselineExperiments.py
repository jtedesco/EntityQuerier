import sys
from experiments.RetrievalExperiment import RetrievalExperiment
from src.queries.builders.AttributeNamesAndValuesQueryBuilder import AttributeNamesAndValuesQueryBuilder
from src.queries.builders.AttributeNamesQueryBuilder import AttributeNamesQueryBuilder
from src.queries.builders.AttributeValuesQueryBuilder import AttributeValuesQueryBuilder
from src.queries.builders.order.WordNetPolysemyQueryBuilder import WordNetPolysemyQueryBuilder
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
            ('YahooKeywords', YahooKeywordQueryBuilder, 50),

            ('WordNetPolysemy10', WordNetPolysemyQueryBuilder, 50),
            ('WordNetPolysemy15', WordNetPolysemyQueryBuilder, 50),
            ('WordNetPolysemy20', WordNetPolysemyQueryBuilder, 50),

#            ('ExactAttributeNames', ExactAttributeNamesQueryBuilder, 50),
#            ('ExactAttributeValues', ExactAttributeValuesQueryBuilder, 50),
#            ('ExactAttributeNamesAndValues', ExactAttributeNamesAndValuesQueryBuilder, 50),
#            ('ApproximateExactAttributeNames', ApproximateExactAttributeNamesQueryBuilder, 50),
#            ('ApproximateExactAttributeValues', ApproximateExactAttributeValuesQueryBuilder, 50),
#            ('ApproximateExactAttributeNamesAndValues', ApproximateExactAttributeNamesAndValuesQueryBuilder, 50),
#            ('ApproximateAttributeNames', ApproximateAttributeNamesQueryBuilder, 50),
#            ('ApproximateAttributeValues', ApproximateAttributeValuesQueryBuilder, 50),
#            ('ApproximateAttributeNamesAndValues', ApproximateAttributeNamesAndValuesQueryBuilder, 50),

#            ('EntityId10', EntityIdQueryBuilder, 10),
#            ('EntityId50', EntityIdQueryBuilder, 50),
#            ('EntityId100', EntityIdQueryBuilder, 100),
#            ('EntityId200', EntityIdQueryBuilder, 200),
#            ('EntityId400', EntityIdQueryBuilder, 400),
#            ('EntityId800', EntityIdQueryBuilder, 800),


#            ('ExactEntityId10', ExactEntityIdQueryBuilder, 10),
#            ('ExactEntityId50', ExactEntityIdQueryBuilder, 50),
#            ('ExactEntityId100', ExactEntityIdQueryBuilder, 100),
#            ('ExactEntityId200', ExactEntityIdQueryBuilder, 200),
#            ('ExactEntityId400', ExactEntityIdQueryBuilder, 400),
#            ('ExactEntityId800', ExactEntityIdQueryBuilder, 800),
#            ('ApproximateEntityId10', ApproximateEntityIdQueryBuilder, 10),
#            ('ApproximateEntityId50', ApproximateEntityIdQueryBuilder, 50),
#            ('ApproximateEntityId100', ApproximateEntityIdQueryBuilder, 100),
#            ('ApproximateEntityId200', ApproximateEntityIdQueryBuilder, 200),
#            ('ApproximateEntityId400', ApproximateEntityIdQueryBuilder, 400),
#            ('ApproximateEntityId800', ApproximateEntityIdQueryBuilder, 800),

#            ('ExactWordNetPolysemy10', ExactWordNetPolysemyQueryBuilder, 50),
#            ('ApproximateExactWordNetPolysemy10', ApproximateExactWordNetPolysemyQueryBuilder, 50),
#            ('ApproximateWordNetPolysemy10', ApproximateWordNetPolysemyQueryBuilder, 50),
        ]

        WordNetPolysemyQueryBuilder.numberOfQueries = 10

        for experiment in experiments:

            print "Number of queries: %d" % WordNetPolysemyQueryBuilder.numberOfQueries

            try:

                # Run experiment
                numberOfSearchResults = experiment[2]
                searchInterface = GoogleSearchFacade(numberOfSearchResults, True)
                retrievalExperiment = RetrievalExperiment(entityId, searchInterface, experiment[1](), numberOfSearchResults)
                retrievalExperiment.run()
                entityName = entityId.replace(' ', '').replace('-', '').replace('\'', '')
                retrievalExperiment.printResults("results/%s/%s" % (entityName, experiment[0]), entityId)

                if 'WordNetPolysemy' in experiment[0]:
                    WordNetPolysemyQueryBuilder.numberOfQueries += 5

            except Exception:
                print "ERROR: " + str(sys.exc_info()[1])
