from json import load
import os
from experiments.RankingExperiment import RankingExperiment
from src.ranking.PL2Ranking import PL2Ranking
from util.RankingExperimentUtil import outputRankingResults

__author__ = 'jon'


if __name__ == '__main__':

    # Find the project root & open the input entity
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]
    entity = load(open(projectRoot + '/entities/Kevin Chen-Chuan Chang.json'))

    # Rank the results
    retrievalResults = '/experiments/retrieval/results/KevinChang-EntityAttributeValues'
    rankingExperiment = RankingExperiment(projectRoot + retrievalResults, entity, PL2Ranking, False, True)
    results = rankingExperiment.rank()

    # Output the ranking results
    entityId = 'Kevin Chen-Chuan Chang'
    outputTitle = "Whoosh PL2 Ranking Results Summary (for top %d results):\n"
    outputFile = 'KevinChang-PL2Ranking'
    outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results)