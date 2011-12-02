import os
import subprocess
from json import load
from experiments.RankingExperiment import RankingExperiment
from src.ranking.BM25Ranking import BM25Ranking
from src.ranking.static.BM25BaselineRanking import BM25BaselineRanking
from src.ranking.static.BM25DescriptionRanking import BM25DescriptionRanking
from src.ranking.static.BM25ExpandedYahooKeywordsRanking import BM25ExpandedYahooKeywordsRanking
from src.ranking.static.BM25HeadersRanking import BM25HeadersRanking
from src.ranking.static.BM25KeywordsRanking import BM25KeywordsRanking
from src.ranking.static.BM25PageRankRanking import BM25PageRankRanking
from src.ranking.static.BM25TitleRanking import BM25TitleRanking
from src.ranking.static.BM25YahooKeywordsRanking import BM25YahooKeywordsRanking
from src.search.extension.BaselineScoreExtension import BaselineScoreExtension
from src.search.extension.ExpandedYQLKeywordExtension import ExpandedYQLKeywordExtension
from src.search.extension.PageRankExtension import PageRankExtension
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from util.RankingExperimentUtil import outputRankingResults

__author__ = 'jon'


if __name__ == '__main__':

    # The entities for which to run the experiments
    entityIds = [
        'ChengXiangZhai'
    ]


    for entityId in entityIds:
#
#        try:
#            output = subprocess.check_call(["rm",  "-rf", ".index"], stderr=subprocess.STDOUT)
#            print "Success rm -rf!"
#        except:
#            pass
#        try:
#            output = subprocess.check_call(["rmdir", ".index"], stderr=subprocess.STDOUT)
#            print "Success rmdir!"
#        except:
#            pass

        # The experiments to run
        experiments = [
            ('BM25BaselineRanking', BM25BaselineRanking),
            ('BM25Ranking', BM25Ranking),
            ('BM25DescriptionRanking', BM25DescriptionRanking),
            ('BM25ExpandedYahooKeywordsRanking', BM25ExpandedYahooKeywordsRanking),
            ('BM25HeadersRanking', BM25HeadersRanking),
            ('BM25KeywordsRanking', BM25KeywordsRanking),
            ('BM25PageRankRanking', BM25PageRankRanking),
            ('BM25TitleRanking', BM25TitleRanking),
            ('BM25YahooKeywordsRanking', BM25YahooKeywordsRanking)
        ]

        for experiment in experiments:

            # Cleanup existing index if it exists

            # Find the project root & open the input entity
            projectRoot = str(os.getcwd())
            projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]
            entity = load(open(projectRoot + '/entities/%s.json' % entityId))

            # Rank the results
            entityName = entityId.replace(' ', '').replace('-', '')
            retrievalResults = '/experiments/retrieval/results/%s/EntityAttributeNamesAndValues' % entityName
            extensions = [
                PageRankExtension(),
                YQLKeywordExtension(),
                ExpandedYQLKeywordExtension(),
                BaselineScoreExtension()
            ]
            rankingExperiment = RankingExperiment(projectRoot + retrievalResults, entity, experiment[1], extensions, False, True)
            results = rankingExperiment.rank()

            # Output the ranking results
            outputTitle = "Results Summary (for top %d results):\n"
            outputFile = entityName + '/' + experiment[0]
            outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results)
