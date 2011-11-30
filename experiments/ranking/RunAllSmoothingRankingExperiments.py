import os, subprocess
from json import load
import sys
from experiments.RankingExperiment import RankingExperiment
from src.ranking.BM25Ranking import BM25Ranking
from src.ranking.smoothing.DMOZSmoothed10000BM25Ranking import DMOZSmoothed10000BM25Ranking
from src.ranking.smoothing.DMOZSmoothed1000BM25Ranking import DMOZSmoothed1000BM25Ranking
from src.ranking.smoothing.DMOZSmoothed100BM25Ranking import DMOZSmoothed100BM25Ranking
from src.ranking.smoothing.DMOZSmoothed5000BM25Ranking import DMOZSmoothed5000BM25Ranking
from src.ranking.smoothing.DMOZSmoothed500BM25Ranking import DMOZSmoothed500BM25Ranking
from src.ranking.smoothing.DMOZSmoothedBM25Ranking import DMOZSmoothedBM25Ranking
from util.RankingExperimentUtil import outputRankingResults

__author__ = 'jon'


if __name__ == '__main__':

    # The entities for which to run the experiments
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

        # The experiments to run
        experiments = [
            ("DMOZSmoothed10000BM25Ranking", DMOZSmoothed10000BM25Ranking),
            ("DMOZSmoothed1000BM25Ranking", DMOZSmoothed1000BM25Ranking),
            ("DMOZSmoothed100BM25Ranking", DMOZSmoothed100BM25Ranking),
            ("DMOZSmoothed5000BM25Ranking", DMOZSmoothed5000BM25Ranking),
            ("DMOZSmoothed500BM25Ranking", DMOZSmoothed500BM25Ranking),
            ("DMOZSmoothedBM25Ranking", DMOZSmoothedBM25Ranking),
            ("BM25Ranking", BM25Ranking)
        ]

        for experiment in experiments:

            print "Running experiment %s for %s" % (experiment[0], entityId)

            # Find the project root & open the input entity
            projectRoot = str(os.getcwd())
            projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]
            entity = load(open(projectRoot + '/entities/%s.json' % entityId))

            # Rank the results
            entityName = entityId.replace(' ', '').replace('-', '')
            retrievalResults = '/experiments/retrieval/results/%s/EntityAttributeNamesAndValues' % entityName
            extensions = []
            rankingExperiment = RankingExperiment(projectRoot + retrievalResults, entity, experiment[1], extensions)
            results = rankingExperiment.rank()

            # Output the ranking results
            outputTitle = "Results Summary (for top %d results):\n"
            outputFile = "dmoz/" + entityName + '/' + experiment[0]
            outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results)

        # Cleanup all the indexes
        output = subprocess.check_call(["rm",  "-rf", ".dmoz-10000-index", ".dmoz-1000-index", ".dmoz-100-index", ".dmoz-5000-index",
                                    ".dmoz-500-index", ".dmoz-index", ".index"])
