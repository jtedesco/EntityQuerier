import sys
from experiments.RetrievalExperiment import RetrievalExperiment
from src.queries.builders.AttributeNamesAndValuesQueryBuilder import AttributeNamesAndValuesQueryBuilder
from src.queries.builders.AttributeNamesQueryBuilder import AttributeNamesQueryBuilder
from src.queries.builders.AttributeValuesQueryBuilder import AttributeValuesQueryBuilder
from src.queries.builders.EntityIdQueryBuilder import EntityIdQueryBuilder
from src.queries.builders.YahooKeywordQueryBuilder import YahooKeywordQueryBuilder
from src.queries.builders.operator.ApproximateAttributeNamesAndValuesQueryBuilder import ApproximateAttributeNamesAndValuesQueryBuilder
from src.queries.builders.operator.ApproximateAttributeNamesQueryBuilder import ApproximateAttributeNamesQueryBuilder
from src.queries.builders.operator.ApproximateAttributeValuesQueryBuilder import ApproximateAttributeValuesQueryBuilder
from src.queries.builders.operator.ApproximateExactAttributeNamesAndValuesQueryBuilder import ApproximateExactAttributeNamesAndValuesQueryBuilder
from src.queries.builders.operator.ApproximateExactAttributeNamesQueryBuilder import ApproximateExactAttributeNamesQueryBuilder
from src.queries.builders.operator.ApproximateExactAttributeValuesQueryBuilder import ApproximateExactAttributeValuesQueryBuilder
from src.queries.builders.operator.ExactAttributeNamesAndValuesQueryBuilder import ExactAttributeNamesAndValuesQueryBuilder
from src.queries.builders.operator.ExactAttributeNamesQueryBuilder import ExactAttributeNamesQueryBuilder
from src.queries.builders.operator.ExactAttributeValuesQueryBuilder import ExactAttributeValuesQueryBuilder
from src.queries.builders.order.WordNetPolysemyQueryBuilder import WordNetPolysemyQueryBuilder
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

            ('ExactAttributeNames', ExactAttributeNamesQueryBuilder, 50),
            ('ExactAttributeValues', ExactAttributeValuesQueryBuilder, 50),
            ('ExactAttributeNamesAndValues', ExactAttributeNamesAndValuesQueryBuilder, 50),
            ('ApproximateExactAttributeNames', ApproximateExactAttributeNamesQueryBuilder, 50),
            ('ApproximateExactAttributeValues', ApproximateExactAttributeValuesQueryBuilder, 50),
            ('ApproximateExactAttributeNamesAndValues', ApproximateExactAttributeNamesAndValuesQueryBuilder, 50),
            ('ApproximateAttributeNames', ApproximateAttributeNamesQueryBuilder, 50),
            ('ApproximateAttributeValues', ApproximateAttributeValuesQueryBuilder, 50),
            ('ApproximateAttributeNamesAndValues', ApproximateAttributeNamesAndValuesQueryBuilder, 50),

            ('EntityId10', EntityIdQueryBuilder, 10),
            ('EntityId50', EntityIdQueryBuilder, 50),
            ('EntityId100', EntityIdQueryBuilder, 100),
            ('EntityId200', EntityIdQueryBuilder, 200),
            ('EntityId400', EntityIdQueryBuilder, 400),
            ('EntityId800', EntityIdQueryBuilder, 800)
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
