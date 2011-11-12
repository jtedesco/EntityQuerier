from json import load
import os
from experiments.RankingExperiment import RankingExperiment
from src.ranking.BaselineResultsRanking import BaselineResultsRanking
from util.RankingExperimentUtil import outputRankingResults

__author__ = 'jon'


if __name__ == '__main__':


   # Find the project root & open the input entity
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]
    entity = load(open(projectRoot + '/entities/Kevin Chen-Chuan Chang.json'))

    # Rank the results
    rankingExperiment = RankingExperiment(projectRoot + '/experiments/retrieval/results/KevinChang-EntityAttributeNamesAndValuesFollowingLinks', entity, BaselineResultsRanking, True, True)
    results = rankingExperiment.rank()

    # Output the ranking results
    entityId = 'Kevin Chen-Chuan Chang'
    baselineTitle = "Baseline Ranking Results Summary (for top %d results):\n"
    outputFile = 'KevinChang-BaselineRanking'
    outputRankingResults(entityId, outputFile, baselineTitle, projectRoot, results)

