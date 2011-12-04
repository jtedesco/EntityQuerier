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
from src.queries.builders.order.ApproximateEntityIdQueryBuilder import ApproximateEntityIdQueryBuilder
from src.queries.builders.order.EntityIdQueryBuilder import EntityIdQueryBuilder
from src.queries.builders.order.ExactEntityIdQueryBuilder import ExactEntityIdQueryBuilder

from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

if __name__ == '__main__':

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
            ('ExactAttributeNames', ExactAttributeNamesQueryBuilder, 50),
            ('ExactAttributeValues', ExactAttributeValuesQueryBuilder, 50),
            ('ExactAttributeNamesAndValues', ExactAttributeNamesAndValuesQueryBuilder, 50),
            ('ApproximateExactAttributeNames', ApproximateExactAttributeNamesQueryBuilder, 50),
            ('ApproximateExactAttributeValues', ApproximateExactAttributeValuesQueryBuilder, 50),
            ('ApproximateExactAttributeNamesAndValues', ApproximateExactAttributeNamesAndValuesQueryBuilder, 50),
            ('ApproximateAttributeNames', ApproximateAttributeNamesQueryBuilder, 50),
            ('ApproximateAttributeValues', ApproximateAttributeValuesQueryBuilder, 50),
            ('ApproximateAttributeNamesAndValues', ApproximateAttributeNamesAndValuesQueryBuilder, 50),
            ('AttributeNames', AttributeNamesQueryBuilder, 50),
            ('AttributeValues', AttributeValuesQueryBuilder, 50),
            ('AttributeNamesAndValues', AttributeNamesAndValuesQueryBuilder, 50),
            ('EntityId10', EntityIdQueryBuilder, 10),
            ('EntityId50', EntityIdQueryBuilder, 50),
            ('EntityId100', EntityIdQueryBuilder, 100),
            ('EntityId200', EntityIdQueryBuilder, 200),
            ('EntityId400', EntityIdQueryBuilder, 400),
            ('EntityId400', EntityIdQueryBuilder, 800),
            ('ExactEntityId10', ExactEntityIdQueryBuilder, 10),
            ('ExactEntityId50', ExactEntityIdQueryBuilder, 50),
            ('ExactEntityId100', ExactEntityIdQueryBuilder, 100),
            ('ExactEntityId200', ExactEntityIdQueryBuilder, 200),
            ('ExactEntityId400', ExactEntityIdQueryBuilder, 400),
            ('ExactEntityId400', ExactEntityIdQueryBuilder, 800),
            ('ApproximateEntityId10', ApproximateEntityIdQueryBuilder, 10),
            ('ApproximateEntityId50', ApproximateEntityIdQueryBuilder, 50),
            ('ApproximateEntityId100', ApproximateEntityIdQueryBuilder, 100),
            ('ApproximateEntityId200', ApproximateEntityIdQueryBuilder, 200),
            ('ApproximateEntityId400', ApproximateEntityIdQueryBuilder, 400),
            ('ApproximateEntityId400', ApproximateEntityIdQueryBuilder, 800)
        ]

        for experiment in experiments:

            # Run experiment
            numberOfSearchResults = experiment[2]
            searchInterface = GoogleSearch(numberOfSearchResults, True)
#            searchInterface.cache = False
            retrievalExperiment = RetrievalExperiment(entityId, searchInterface, experiment[1](), numberOfSearchResults)
            retrievalExperiment.run()
            retrievalExperiment.printResults("results/%s/%s" % (entityName, experiment[0]), entityId)
