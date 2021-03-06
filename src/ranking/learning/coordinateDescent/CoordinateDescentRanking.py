import os
import sys
from copy import deepcopy
from json import load
from pprint import pprint
from threading import Lock
from src.ranking.learning.coordinateDescent.CoordinateDescentRankingThread import CoordinateDescentRankingThread
from src.search.extension.BaselineScoreExtension import BaselineScoreExtension
from src.search.extension.ExpandedYQLKeywordExtension import ExpandedYQLKeywordExtension
from src.search.extension.PageRankExtension import PageRankExtension
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from src.util.RankingExperimentUtililty import getKeywords, outputRankingResults

__author__ = 'jon'

class CoordinateDescentRanking(object):
    """
      Represents a ranking system using a set of keywords and a set of search results to rerank them.
    """

    @staticmethod
    def getIndexLocation():
        return "/home/jon/Documents/.index"


    def __init__(self, keywords, relevantResults):
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
            'baselineScore' : 0.1,      # A constant added to the final score
            'pageRank' : 0.1,           # A constant offset based on PR
            'pageRankScaling' : 0.1     # Scaling factor based on PR, if weighting is 0, score will be unchanged)
        }

        # The initial guesses at the feature's weightings (starts at 1.0 for most), and
        self.values = {
         'content' : 1.0,
         'title' : 1.0,
         'keywords' : 1.0,
         'headers' : 1.0,
         'description' : 1.0,
         'yqlKeywords' : 1.0,
         'expandedYqlKeywords' : 1.0,
         'baselineScore' : 0.5,      # Weight between baseline score & computed score
         'pageRank' : 1.0,           # A constant offset based on PR
         'pageRankScaling' : 1.0     # Scaling factor based on PR, if weighting is 0, score will be unchanged)
        }

        self.keywords = keywords
        self.relevantResults = relevantResults


    def learn(self):
        """
          Run the learning algorithm, and return the learned feature weights
        """

        # Get a copy of the values to tweak
        values = deepcopy(self.values)

        # Get the current scoring
        changes = {
            'lock' : Lock()
        }
        print "about to start learning"
        scoringThread = CoordinateDescentRankingThread(values, self.keywords, changes, 'original',
                                                       self.relevantResults, CoordinateDescentRanking.getIndexLocation() + '-original')
        scoringThread.start()
        scoringThread.join()
        currentWeightingScoring = changes['original']
        print "Original scoring: %1.5f" % currentWeightingScoring

        # The set of features to still tweak
        features = self.values.keys()

        # Keep looping until no further change is necessary
        complete = False
        iterations = 0
        while not complete:

            complete = True
            iterations += 1

            # Create data structures for managing threads
            changes = {
                'lock' : Lock()
            }
            threads = []

            # Launch threads to test changes to each feature weight
            print "Preparing threads..."
            for feature in features:

                # Form the path to the index to use for this test
                featureIndexLocation = CoordinateDescentRanking.getIndexLocation() + '-' + feature

                # Launch test for increasing weight of this feature
                values = deepcopy(self.values)
                values[feature] += self.stepSizes[feature]
                scoringThread = CoordinateDescentRankingThread(values, self.keywords, changes, feature + '+',
                                                               self.relevantResults, featureIndexLocation)
                threads.append(scoringThread)

                # Launch test for decreasing weight of this feature
                values = deepcopy(self.values)
                values[feature] -= self.stepSizes[feature]
                scoringThread = CoordinateDescentRankingThread(values, self.keywords, changes, feature + '-',
                                                               self.relevantResults, featureIndexLocation)
                threads.append(scoringThread)


            print "Launching threads..."
            for thread in threads:
                thread.start()

            # Wait for all threads to finish
            print "Waiting for threads to finish..."
            for thread in threads:
                thread.join()

            # Update feature weights accordingly
            print "Analyzing ranking results"
            for feature in deepcopy(features):

                increaseFeatureWeightResultScoring = changes[feature+'+']
                decreaseFeatureWeightResultScoring = changes[feature+'-']

                # If one of these improved...
                if increaseFeatureWeightResultScoring > currentWeightingScoring or decreaseFeatureWeightResultScoring > currentWeightingScoring:
                    if increaseFeatureWeightResultScoring > decreaseFeatureWeightResultScoring:
                        self.values[feature] += self.stepSizes[feature]
                    elif decreaseFeatureWeightResultScoring >= increaseFeatureWeightResultScoring:
                        self.values[feature] -= self.stepSizes[feature]
                    complete = False
                else:
                    del features[feature]
                    print "No improvement found for tweaking %s!" % feature

            print "Finished learning iteration %d, new values:" % iterations
            pprint(self.values)


    def rank(self):
        """
          Perform the ranking with the given parameters
        """

        values = deepcopy(self.values)

        # Get the current scoring
        changes = {
            'lock' : Lock()
        }
        scoringThread = CoordinateDescentRankingThread(values, self.keywords, changes, 'original', self.relevantResults,
                                                       CoordinateDescentRanking.getIndexLocation() + '-original')
        scoringThread.start()
        scoringThread.join()
        results = scoringThread.results

        return results


if __name__ == '__main__':

    if not os.path.exists(CoordinateDescentRanking.getIndexLocation() + '-original'):
        print "Cannot find index location!"
        sys.exit()

    retrievalTest = 'ExactAttributeNamesAndValues'
    experiment = ('CoordinateDescentRanking', CoordinateDescentRanking)

    # Indicates whether to perform the learning or ranking phase
    finalValues = None

    # The entity ids to use
    entityIds = [
#        "ChengXiang Zhai",
#        "Danny Dig",
        "Kevin Chen-Chuan Chang",
#        "Paris Smaragdis",
#        "Matthew Caesar",
#        "Ralph Johnson",
#        "Robin Kravets"
    ]

    keywords = {}
    relevantResults = {}

    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]

    for entityId in entityIds:

        # Find the project root & open the input entity
        entity = load(open(projectRoot + '/entities/%s.json' % entityId))

        # The extensions to use to gather results
        extensions = [
            PageRankExtension(),
            YQLKeywordExtension(),
            ExpandedYQLKeywordExtension(),
            BaselineScoreExtension()
        ]

        # Get & store the results for this entity
        entityName = entityId.replace(' ', '').replace('-', '').replace('\'', '')
        retrievalResultsPath = projectRoot + '/experiments/retrieval/results/%s/%s' % (entityName, retrievalTest)

        # Store the relevant results for this entity
        relevantResults[entityId] = load(open(projectRoot + '/entities/relevanceStandard/' + entityId + '.json'))

        # Build the keywords for this entity
        keywords[entityId] = getKeywords(entity)

    # Perform the learned ranking if we haven't, or generate the final ranking if we have
    if finalValues is None:

        # Learn the ranking
        ranking = CoordinateDescentRanking(keywords, relevantResults)
        values = ranking.learn()

        print "Final Values:"
        pprint(values)

    else:

        # Perform the ranking
        ranking = CoordinateDescentRanking(keywords, relevantResults)
        ranking.values = finalValues
        results = ranking.rank()

        for entityId in entityIds:

            entityName = entityId.replace(' ', '').replace('-', '').replace('\'', '')

            # Output the ranking results
            outputTitle = "Results Summary (for top %d results):\n"
            outputFile = entityName + '-' + experiment[0]
            outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results)
