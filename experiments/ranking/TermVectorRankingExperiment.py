from json import load
import os
from experiments.RankingExperiment import RankingExperiment
from src.ranking.TermVectorRanking import TermVectorRanking
from util.RankingExperimentUtil import outputRankingResults

__author__ = 'jon'


if __name__ == '__main__':

    # Find the project root & open the input entity
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]
    entity = load(open(projectRoot + '/entities/Kevin Chen-Chuan Chang.json'))

    # Rank the results
    rankingExperiment = RankingExperiment(projectRoot + '/experiments/retrieval/results/KevinChang-EntityValuesOnly', entity, TermVectorRanking)
    results = rankingExperiment.rank()

    # Output the ranking results
    outputFile = 'KevinChang-TermVectorRanking'
    entityId = 'Kevin Chen-Chuan Chang'
    outputTitle = "Term Vector Ranking Results Summary (for top %d results):\n"
    outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results)
    
