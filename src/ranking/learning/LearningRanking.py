from IN import INT_MAX
from copy import deepcopy
from json import load
import os
from pprint import pprint
import whoosh
from whoosh.qparser.default import MultifieldParser
from whoosh.qparser.plugins import PlusMinusPlugin
from whoosh.qparser.syntax import OrGroup
from experiments.RankingExperiment import RankingExperiment
from src.ranking.BM25Ranking import BM25Ranking
from src.ranking.learning.LearningScorer import LearningScorer
from src.search.extension.ExpandedYQLKeywordExtension import ExpandedYQLKeywordExtension
from src.search.extension.PageRankExtension import PageRankExtension
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from util.RankingExperimentUtil import getRankingResults, outputRankingResults

__author__ = 'jon'

class LearningRanking(BM25Ranking):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    def __init__(self, searchResults, keywords):
        """
          Initializes data structures for the learning algorithm
        """

        # The step sizes to take for each feature's weighting
        self.stepSizes = {
            'content' : 0.1,
            'title' : 0.1,
            'keywords' : 0.1,
            'headers' : 0.1,
            'description' : 0.1,
            'yqlKeywords' : 0.1,
            'expandedYqlKeywords' : 0.1,
            'pageRank' : 0.1,           # A constant offset based on PR
            'pageRankScaling' : 0.1     # Scaling factor based on PR, if weighting is 0, score will be unchanged)
        }

        # The initial guesses at the feature's weightings (starts at 1.0), and
        self.values = {
            'content' : 1.0,
            'title' : 1.0,
            'keywords' : 1.0,
            'headers' : 1.0,
            'description' : 1.0,
            'yqlKeywords' : 1.0,
            'expandedYqlKeywords' : 1.0,
            'pageRank' : 1.0,           # A constant offset based on PR
            'pageRankScaling' : 1.0     # Scaling factor based on PR, if weighting is 0, score will be unchanged)
        }
        self.testValues = deepcopy(self.values)

        # Find the project root
        projectRoot = str(os.getcwd())
        projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]

        # Prepare the list of relevant results (golden standard for each entity)
        self.entityId = 'Kevin Chen-Chuan Chang'
        self.relevantResults = load(open(projectRoot + '/standard/' + entityId + '.json'))

        # Cache the parsed query
        self.query = None

        super(LearningRanking, self).__init__(searchResults, keywords)


    def queryIndex(self, weightingMechanism):
        """
          Query the index, given the current scoring guess
        """

        # Create a searcher object for this index
        searcher = self.index.searcher(weighting=weightingMechanism)

        # Create a query parser, providing it with the schema of this index, and the default field to search, 'content'
        termBoosts = deepcopy(self.testValues)
        del termBoosts['pageRank']
        del termBoosts['pageRankScaling']
        LearningScorer.pageRankWeight = self.testValues['pageRank']
        LearningScorer.pageRankScalingWeight = self.testValues['pageRankScaling']
        keywordsQueryParser = MultifieldParser(['content', 'title', 'description', 'keywords', 'headers', 'yqlKeywords', 'expandedYqlKeywords'],
                self.indexSchema, fieldboosts=termBoosts, group=OrGroup)
        keywordsQueryParser.add_plugin(PlusMinusPlugin)
        if self.query is None:
            query = "+\"" + self.entityId + "\" "
            for keyword in self.keywords:
                if keyword != self.entityId:
                    query += "\"" + keyword + "\" "
            query = query.rstrip()
        else:
            query = self.query
        queryObject = keywordsQueryParser.parse(query)

        # Perform the query itself
        try:
            searchResults = searcher.search(queryObject, INT_MAX)
        except whoosh.reading.TermNotFound:
            print "Term not found!"
            searchResults = []

        # Format the results
        results = []
        for searchResult in searchResults:

            result = {
                'url': searchResult['url'],
                'content': searchResult['content'],
                'title': searchResult['title'],
                'description': searchResult['description'],
                'keywords': searchResult['keywords'],
                'headers': searchResult['headers'],
                'yqlKeywords': searchResult['yqlKeywords'],
                'expandedYqlKeywords': searchResult['expandedYqlKeywords'],
                'pageRank': searchResult['pagerank']
            }
            results.append(result)

        # Return the list of web pages along with the terms used in the search
        return results


    def evaluateResults(self, results, relevantResults):
        """
          Returns a score based on the results, specifically computing recall, precision, and avg precision
        """

        recallAt10, recallAt20, recallAt50, recallAt100, precisionAt10, precisionAt20, precisionAt50, precisionAt100, \
            averagePrecisionAt10, averagePrecisionAt20, averagePrecisionAt50, averagePrecisionAt100 = getRankingResults(results, relevantResults, 101)

        # Multiply metrics together (any extremely low scores at one level should make big impact on score)
        score = (recallAt10 * precisionAt10 * averagePrecisionAt10) + (recallAt20 * precisionAt20 * averagePrecisionAt20) + \
                (recallAt50 * precisionAt50 * averagePrecisionAt50) + (recallAt100 * precisionAt100 * averagePrecisionAt100)

        return score


    def actuallyRank(self):

        reRankedResults = self.queryIndex(LearningScorer)
        return reRankedResults


    def rank(self):
        """
          Run the learning algorithm, and return the learned feature weights
        """

        # Get a copy of the values to tweak
        newValues = deepcopy(self.values)

        # Keep looping until no further change is necessary
        complete = False
        while not complete:

            complete = True
            for feature in newValues:

                pprint(newValues)

                # Get the current scoring
                rankingResults = self.actuallyRank()
                currentWeightingScoring = self.evaluateResults(rankingResults, self.relevantResults)

                # Evaluate effect of increase in weight of this features
                testValues = deepcopy(newValues)
                testValues[feature] += self.stepSizes[feature]
                self.testValues = testValues
                rankingResults = self.actuallyRank()
                increaseFeatureWeightResultScoring = self.evaluateResults(rankingResults, self.relevantResults)

                # Evaluate effect of decrease in weight of this features
                testValues = deepcopy(newValues)
                testValues[feature] -= self.stepSizes[feature]
                self.testValues = testValues
                rankingResults = self.actuallyRank()
                decreaseFeatureWeightResultScoring = self.evaluateResults(rankingResults, self.relevantResults)

                # Update the weighting vector if one of these was an improvement
                if increaseFeatureWeightResultScoring > currentWeightingScoring:
                    complete = False
                    newValues[feature] += self.stepSizes[feature]
                elif decreaseFeatureWeightResultScoring > currentWeightingScoring:
                    complete = False
                    newValues[feature] -= self.stepSizes[feature]
                else:
                    # If no change was made, don't update anything
                    pass

                for feature in newValues:
                    newValues[feature] = round(newValues[feature], 2)
                
            print "Finished one learning iteration"

        self.testValues = newValues
        self.values = newValues
        results = BM25Ranking.rank(self)

        return results


if __name__ == '__main__':
    
    experiment = ('LearningRanking', LearningRanking)

    entityId = 'Kevin Chen-Chuan Chang'

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
    rankingExperiment = RankingExperiment(projectRoot + retrievalResults, entity, experiment[1], extensions, False, True)
    results = rankingExperiment.rank()

    # Output the ranking results
    outputTitle = "Results Summary (for top %d results):\n"
    outputFile = entityName + '-' + experiment[0]
    outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results)
    