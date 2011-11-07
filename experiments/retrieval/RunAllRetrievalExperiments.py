from experiments.retrieval.EntityAttributeNamesAndValuesQueryExperiment import EntityAttributeNamesAndValues
from experiments.retrieval.EntityAttributeNamesAndValuesQueryWithOperatorsAndFollowingLinksAndKeywordExperiment import EntityAttributeNamesValuesOperatorsFollowingLinksAndKeyword
from experiments.retrieval.EntityAttributeNamesAndValuesQueryWithOperatorsAndFollowingLinksExperiment import EntityAttributeNamesValuesOperatorsAndFollowingLinks
from experiments.retrieval.EntityAttributeNamesAndValuesQueryWithOperatorsAndKeywordExperiment import EntityAttributeNamesValuesOperatorsAndKeywords
from experiments.retrieval.EntityAttributeNamesAndValuesQueryWithOperatorsExperiment import EntityAttributeNamesValuesAndOperators
from experiments.retrieval.EntityAttributeNamesQueryExperiment import EntityAttributeNames
from experiments.retrieval.EntityAttributeValuesQueryExperiment import EntityAttributeValues

__author__ = 'jon'


if __name__ == '__main__':

    # Attribute names only
    experiment = EntityAttributeNames()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeNames")

    # Attribute values only
    experiment = EntityAttributeValues()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeValues")

    # Attribute names & values
    experiment = EntityAttributeNamesAndValues()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeNamesAndValues")

    # Attribute names & values + query operators
    experiment = EntityAttributeNamesValuesAndOperators()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeNamesValuesAndOperators")

    # Attribute names & values + link crawling
    experiment = EntityAttributeNamesValuesOperatorsAndFollowingLinks()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeNamesValuesOperatorsFollowingLinksAndKeywords")

    # Attribute names & values + top result keywords
    experiment = EntityAttributeNamesValuesOperatorsAndKeywords()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityNamesAndValuesWithOperatorsAndKeywords")

    # Attribute names & values + keywords + link crawling
    experiment = EntityAttributeNamesValuesOperatorsFollowingLinksAndKeyword()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityNamesAndValuesWithOperatorsAndFollowingLinksAndKeywords")

    