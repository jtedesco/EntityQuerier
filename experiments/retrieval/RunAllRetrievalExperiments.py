from experiments.RetrievalExperiment import RetrievalExperiment
from src.queries.builders.operator.ApproximateAttributeNamesAndValuesQueryBuilder import ApproximateAttributeNamesAndValuesQueryBuilder
from src.queries.builders.operator.ApproximateAttributeNamesQueryBuilder import ApproximateAttributeNamesQueryBuilder
from src.queries.builders.operator.ApproximateAttributeValuesQueryBuilder import ApproximateAttributeValuesQueryBuilder
from src.queries.builders.operator.ApproximateExactAttributeNamesAndValuesQueryBuilder import ApproximateExactAttributeNamesAndValuesQueryBuilder
from src.queries.builders.operator.ApproximateExactAttributeNamesQueryBuilder import ApproximateExactAttributeNamesQueryBuilder
from src.queries.builders.operator.ApproximateExactAttributeValuesQueryBuilder import ApproximateExactAttributeValuesQueryBuilder
from src.queries.builders.operator.AttributeNamesAndValuesQueryBuilder import AttributeNamesAndValuesQueryBuilder
from src.queries.builders.operator.AttributeNamesQueryBuilder import AttributeNamesQueryBuilder
from src.queries.builders.operator.AttributeValuesQueryBuilder import AttributeValuesQueryBuilder
from src.queries.builders.operator.ExactAttributeNamesAndValuesQueryBuilder import ExactAttributeNamesAndValuesQueryBuilder
from src.queries.builders.operator.ExactAttributeNamesQueryBuilder import ExactAttributeNamesQueryBuilder
from src.queries.builders.operator.ExactAttributeValuesQueryBuilder import ExactAttributeValuesQueryBuilder

from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

if __name__ == '__main__':

    numberOfSearchResults = 50
    entityIds = [
        "ChengXiang Zhai",
        "Danny Dig",
        "Kevin Chen-Chuan Chang",
        "Paris Smaragdis",
        "Matthew Caesar",
        "Ralph Johnson",
        "Robin Kravets"
    ]

    for entityId in entityIds:

        entityName = entityId.replace(' ', '')
        entityName = entityName.replace('-', '')

        experiments = [
            ('ExactAttributeNames', ExactAttributeNamesQueryBuilder),
            ('ExactAttributeValues', ExactAttributeValuesQueryBuilder),
            ('ExactAttributeNamesAndValues', ExactAttributeNamesAndValuesQueryBuilder),
            ('ApproximateExactAttributeNames', ApproximateExactAttributeNamesQueryBuilder),
            ('ApproximateExactAttributeValues', ApproximateExactAttributeValuesQueryBuilder),
            ('ApproximateExactAttributeNamesAndValues', ApproximateExactAttributeNamesAndValuesQueryBuilder),
            ('ApproximateAttributeNames', ApproximateAttributeNamesQueryBuilder),
            ('ApproximateAttributeValues', ApproximateAttributeValuesQueryBuilder),
            ('ApproximateAttributeNamesAndValues', ApproximateAttributeNamesAndValuesQueryBuilder),
            ('AttributeNames', AttributeNamesQueryBuilder),
            ('AttributeValues', AttributeValuesQueryBuilder),
            ('AttributeNamesAndValues', AttributeNamesAndValuesQueryBuilder)
        ]

        for experiment in experiments:

            # Run experiment
            searchInterface = GoogleSearch(numberOfSearchResults, True)
            retrievalExperiment = RetrievalExperiment(entityId, searchInterface, experiment[1](), numberOfSearchResults)
            retrievalExperiment.run()
            retrievalExperiment.printResults("results/%s/%s" % (entityName, experiment[0]), entityId)