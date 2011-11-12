from experiments.retrieval.EntityAttributeNames import EntityAttributeNames
from experiments.retrieval.EntityAttributeNamesAndValues import EntityAttributeNamesAndValues
from experiments.retrieval.EntityAttributeNamesAndValuesFollowingLinks import EntityAttributeNamesAndValuesFollowingLinks
from experiments.retrieval.EntityAttributeValues import EntityAttributeValues
from experiments.retrieval.EntityAttributeValuesFollowingLinks import EntityAttributeValuesFollowingLinks

_author__ = 'jon'


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

    # Attribute values  & following links
    experiment = EntityAttributeValuesFollowingLinks()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeValuesFollowingLinks")

    # Attribute names & values + link crawling
    experiment = EntityAttributeNamesAndValuesFollowingLinks()
    experiment.run()
    experiment.printResults("results/KevinChang-EntityAttributeNamesAndValuesFollowingLinks")
    