from json import load
import os
from experiments.RankingExperiment import RankingExperiment
from src.ranking import WeightedTitleKeywordsDescriptionPageRankBM25Ranking
from util.RankingExperimentUtil import outputRankingResults

__author__ = 'jon'


if __name__ == '__main__':

    # Find the project root & open the input entity
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]
    entity = load(open(projectRoot + '/entities/Kevin Chen-Chuan Chang.json'))

    # Rank the results
    retrievalResults = '/experiments/retrieval/results/KevinChang-EntityAttributeNamesAndValuesFollowingLinks'
    rankingExperiment = RankingExperiment(projectRoot + retrievalResults, entity, WeightedTitleKeywordsDescriptionPageRankBM25Ranking, False, True)
    results = rankingExperiment.rank()

    # Output the ranking results
    entityId = 'Kevin Chen-Chuan Chang'
    outputTitle = "Whoosh Frequency Ranking Results Summary (for top %d results):\n"
    outputFile = 'KevinChang-WeightedTitleKeywordsDescriptionPageRankBM25Ranking'
    outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results)