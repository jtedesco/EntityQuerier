from experiments.professors.EntityAttributeNamesAndValuesQueryExperiment import EntityAttributeNamesAndValuesQueryExperiment
from experiments.professors.EntityAttributeNamesAndValuesQueryWithOperatorsExperiment import EntityAttributeNamesAndValuesQueryWithOperatorsExperiment
from experiments.professors.EntityAttributeNamesQueryExperiment import EntityAttributeNamesQueryExperiment
from experiments.professors.EntityAttributeValuesQueryExperiment import EntityAttributeValuesQueryExperiment

__author__ = 'jon'


if __name__ == '__main__':

    # Attribute names only
    experiment = EntityAttributeNamesQueryExperiment()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityNamesOnly")

    # Attribute values only
    experiment = EntityAttributeValuesQueryExperiment()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityValuesOnly")

    # Attribute names & values
    experiment = EntityAttributeNamesAndValuesQueryExperiment()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityNamesAndValues")

    # Attribute names & values + query operators
    experiment = EntityAttributeNamesAndValuesQueryWithOperatorsExperiment()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityNamesAndValuesWithOperators")

    # Attribute names & values + link crawling

    # Attribute names & values + top result keywords

    # Attribute names & values + keywords + link crawling


    