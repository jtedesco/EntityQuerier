import sys
from experiments.RetrievalExperiment import RetrievalExperiment
from src.queries.builders.operator.ApproximateAttributeNamesAndValuesQueryBuilder import ApproximateAttributeNamesAndValuesQueryBuilder
from src.queries.builders.operator.ApproximateAttributeNamesQueryBuilder import ApproximateAttributeNamesQueryBuilder
from src.queries.builders.operator.ApproximateAttributeValuesQueryBuilder import ApproximateAttributeValuesQueryBuilder
from src.queries.builders.operator.ApproximateExactAttributeNamesAndValuesQueryBuilder import ApproximateExactAttributeNamesAndValuesQueryBuilder
from src.queries.builders.operator.ApproximateExactAttributeNamesQueryBuilder import ApproximateExactAttributeNamesQueryBuilder
from src.queries.builders.operator.ApproximateExactAttributeValuesQueryBuilder import ApproximateExactAttributeValuesQueryBuilder
from src.queries.builders.operator.ExactAttributeNamesAndValuesQueryBuilder import ExactAttributeNamesAndValuesQueryBuilder
from src.queries.builders.operator.ExactAttributeNamesQueryBuilder import ExactAttributeNamesQueryBuilder
from src.queries.builders.operator.ExactAttributeValuesQueryBuilder import ExactAttributeValuesQueryBuilder
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
            ('ExactAttributeNames', ExactAttributeNamesQueryBuilder, 50),
            ('ExactAttributeValues', ExactAttributeValuesQueryBuilder, 50),
            ('ExactAttributeNamesAndValues', ExactAttributeNamesAndValuesQueryBuilder, 50),
            ('ApproximateExactAttributeNames', ApproximateExactAttributeNamesQueryBuilder, 50),
            ('ApproximateExactAttributeValues', ApproximateExactAttributeValuesQueryBuilder, 50),
            ('ApproximateExactAttributeNamesAndValues', ApproximateExactAttributeNamesAndValuesQueryBuilder, 50),
            ('ApproximateAttributeNames', ApproximateAttributeNamesQueryBuilder, 50),
            ('ApproximateAttributeValues', ApproximateAttributeValuesQueryBuilder, 50),
            ('ApproximateAttributeNamesAndValues', ApproximateAttributeNamesAndValuesQueryBuilder, 50)
        ]

        for experiment in experiments:

            try:

                # Run experiment
                numberOfSearchResults = experiment[2]
                searchInterface = GoogleSearchFacade(numberOfSearchResults, True)
                retrievalExperiment = RetrievalExperiment(entityId, searchInterface, experiment[1](), numberOfSearchResults)
                retrievalExperiment.run()
                entityName = entityId.replace(' ', '').replace('-', '').replace('\'', '')
                retrievalExperiment.printResults("results/%s/%s" % (entityName, experiment[0]), entityId)

            except Exception:
                print "ERROR: " + str(sys.exc_info()[1])
