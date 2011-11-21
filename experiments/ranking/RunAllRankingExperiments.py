from json import load
import os
from experiments.RankingExperiment import RankingExperiment
from src.ranking.BM25Ranking import BM25Ranking
from src.ranking.PageRankBM25Ranking import PageRankBM25Ranking
from src.ranking.TFIDFRanking import TFIDFRanking
from src.ranking.TermFrequencyRanking import TermFrequencyRanking
from src.ranking.WeightedHeadersPageRankBM25Ranking import WeightedHeadersPageRankBM25Ranking
from src.ranking.WeightedHeadersTitleKeywordsPageRankBM25Ranking import WeightedHeadersTitleKeywordsPageRankBM25Ranking
from src.ranking.WeightedHeadersTitlePageRankBM25Ranking import WeightedHeadersTitlePageRankBM25Ranking
from src.ranking.WeightedTitleKeywordsDescriptionPageRankBM25Ranking import WeightedTitleKeywordsDescriptionPageRankBM25Ranking
from src.ranking.WeightedTitlePageRankBM25Ranking import WeightedTitlePageRankBM25Ranking
from src.ranking.WeightedTitleYQLKeywordsPageRankBM25Ranking import WeightedTitleYQLKeywordsPageRankBM25Ranking
from src.search.extension.ExpandedYQLKeywordExtension import ExpandedYQLKeywordExtension
from src.search.extension.PageRankExtension import PageRankExtension
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from util.RankingExperimentUtil import outputRankingResults

__author__ = 'jon'


if __name__ == '__main__':

    # The entities for which to run the experiments
    entityIds = [
        'Kevin Chen-Chuan Chang'
    ]


    for entityId in entityIds:

        # The experiments to run
        experiments = [
            ('BM25Ranking', BM25Ranking),
            ('PageRankBM25Ranking', PageRankBM25Ranking),
            ('TermFrequencyRanking', TermFrequencyRanking),
            ('TFIDFRanking', TFIDFRanking),
            ('WeightedHeadersPageRankBM25Ranking', WeightedHeadersPageRankBM25Ranking),
            ('WeightedHeadersTitleKeywordsPageRankBM25Ranking', WeightedHeadersTitleKeywordsPageRankBM25Ranking),
            ('WeightedHeadersTitlePageRankBM25Ranking', WeightedHeadersTitlePageRankBM25Ranking),
            ('WeightedTitleKeywordsDescriptionPageRankBM25Ranking', WeightedTitleKeywordsDescriptionPageRankBM25Ranking),
            ('WeightedTitlePageRankBM25Ranking', WeightedTitlePageRankBM25Ranking),
            ('WeightedTitleYQLKeywordsPageRankBM25Ranking', WeightedTitleYQLKeywordsPageRankBM25Ranking)
        ]

        for experiment in experiments:
        
            # Find the project root & open the input entity
            projectRoot = str(os.getcwd())
            projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]
            entity = load(open(projectRoot + '/entities/%s.json' % entityId))

            # Rank the results
            entityName = entityId.replace(' ', '').replace('-', '')
            retrievalResults = '/experiments/retrieval/results/%s-EntityAttributeNamesAndValues' % entityName
            extensions = [
                PageRankExtension(),
                YQLKeywordExtension(),
                ExpandedYQLKeywordExtension()
            ]
            includeOriginalResults = experiment[0] == 'Baseline'
            rankingExperiment = RankingExperiment(projectRoot + retrievalResults, entity, experiment[1], extensions, includeOriginalResults, True)
            results = rankingExperiment.rank()

            # Output the ranking results
            outputTitle = "Results Summary (for top %d results):\n"
            outputFile = entityName + '-' + experiment[0]
            outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results)
