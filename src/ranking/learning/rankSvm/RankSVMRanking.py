import os
import subprocess
from json import load
from src.search.extension.BaselineScoreExtension import BaselineScoreExtension
from src.search.extension.PageRankExtension import PageRankExtension
from src.util.RankingExperimentUtililty import outputRankingResults, scoreResults
from src.util.ResultsBuilderUtility import  getExtensionsResultsFromRetrievalFile, getResultsUrlsFromRetrievalFile

__author__ = 'jon'


class RankSVMRanking(object):
    """
      Ranking scheme that uses RankSVM to learn a ranking for each entity
    """

    rankSVMPath = '/opt/svm-rank/'
    trainingFilePath = 'trainingFile'


    def __init__(self, searchResults, relevance, features):
        """
          Initializes this ranking object, taking in a dictionary of entity ids to search results and the relevance
            information for each entity

            @param  searchResults   The map of search results for each entities
            @param  relevance       The relevance standard for each entity
            @param  features        The vector of features supported in the search results (list of result ids)
        """

        self.searchResults = searchResults
        self.relevance = relevance
        self.features = features


    def buildRankSVMRankingInput(self, qid, rankSVMData, scoredResult, relevantURLs = {}):
        """
          Helps build the string for an entity given a scored search result

            @param  qid             The id number of the query
            @param  rankSVMData     The data generated so far
            @param  scoredResult    The scored search result
            @param  relevantURLs    The relevance set of urls (empty if unknown)
        """

        if 'url' in scoredResult:

            # The RankSVM relevance label
            preferenceScore = 0
            if str(scoredResult['url']) in relevantURLs:
                preferenceScore = 1

            # build the training line
            lineData = "%d qid:%d" % (preferenceScore, qid)
            for index in xrange(0, len(self.features)):
                feature = self.features[index]

                # Extract the data for this feature
                try:
                    data = scoredResult[feature]
                except KeyError:
                    print "Missing '%s' for '%s'" % (feature, scoredResult['url'])
                    data = 0.0

                # Add the line data
                lineData += " %d:%1.2f" % (index + 1, float(data))

            rankSVMData += lineData + '   #%s \n' % scoredResult['url']

        return rankSVMData


    def learn(self):
        """
          Train the ranking algorithm using the search results and relevance guide
        """

        rankSVMTrainingData = ""

        qid = 1
        for entityId in self.searchResults:

            # Get the set of relevant URLs for this entity
            relevantURLs = set(self.relevance[entityId])

            # Add a title for the query training section
            rankSVMTrainingData += "# Entity '%s'\n" % entityId

            for searchResults in self.searchResults[entityId]:
                rankSVMTrainingData = self.buildRankSVMRankingInput(qid, rankSVMTrainingData, searchResults, relevantURLs)

            qid +=1

        # Dump the data to the training file
        trainingDataPath = 'trainingData'
        if os.path.exists(trainingDataPath):
            os.remove(trainingDataPath)
        open(trainingDataPath, 'w').write(rankSVMTrainingData)

        # Remove training file
        if os.path.exists(RankSVMRanking.trainingFilePath):
            os.remove(RankSVMRanking.trainingFilePath)

        # Train RankSVM model
        subprocess.Popen([RankSVMRanking.rankSVMPath + 'svm_rank_learn', '-c', '3', trainingDataPath,
                          RankSVMRanking.trainingFilePath]).communicate()
        


    def rank(self, scoredResults, entityId):
        """
          Rank the scored results of a single entity
        """

        # Remove the test input file if it exists
        testInputPath = 'testInput'
        if os.path.exists(testInputPath):
            os.remove(testInputPath)

        # Build the formatted input data
        rankSVMInputData = "# Entity '%s'\n" % entityId
        for searchResult in scoredResults:
            rankSVMInputData = self.buildRankSVMRankingInput(0, rankSVMInputData, searchResult)
        open(testInputPath, 'w').write(rankSVMInputData)

        # Remove the test output file if it exists
        testOutputPath = 'testData'
        if os.path.exists(testOutputPath):
            os.remove(testOutputPath)

        # Run RankSVM
        subprocess.Popen([RankSVMRanking.rankSVMPath + 'svm_rank_classify', testInputPath, RankSVMRanking.trainingFilePath,
                          testOutputPath]).communicate()

        # Get the scores
        stringScores = open(testOutputPath).read().split('\n')
        scores = []
        for stringScore in stringScores:
            if len(stringScore) > 0:
                scores.append(float(stringScore.strip()))

        # Sort by scores
        scoresAndResults = zip(scores, scoredResults)
        scoresAndResults.sort(reverse=True)

        # Collect reranked results
        reRankedResults = list(zip(*scoresAndResults)[1])

        return reRankedResults


if __name__ == '__main__':

    features = [
         'content',
         'title',
         'keywords',
         'headers',
         'description',
         'yqlKeywords',
         'expandedYqlKeywords',
         'baselineScore',
         'pageRank'
    ]

    entityIds = [
        "ChengXiang Zhai",
        "Danny Dig",
        "Kevin Chen-Chuan Chang",
        "Paris Smaragdis",
        "Matthew Caesar",
        "Ralph Johnson",
        "Robin Kravets"
    ]

    # Find the project root
    projectRoot = str(os.getcwd())
    projectRoot = projectRoot[:projectRoot.find('EntityQuerier') + len('EntityQuerier')]

    # Build the relevance sets for each
    retrievalExperimentResults = 'AttributeNamesAndValues'
    scoredResults = {}
    relevance = {}

    # If the training file doesn't exist, perform the learning stage
    learn = True

    for entityId in entityIds:

        print "Gathering scored results"

        # Get the entity
        entity = load(open(projectRoot + '/entities/%s.json' % entityId))
        if learn:
            relevance[entityId] = load(open(projectRoot + '/entities/relevanceStandard/%s.json' % entityId))
        else:
            relevance[entityId] = {}

        # The extensions for results
        extensions = [
            PageRankExtension(),
            BaselineScoreExtension()
        ]

        # Get the retrieval results for this entity
        entityName = entityId.replace(' ', '').replace('-', '')
        resultsFilePath = projectRoot + '/experiments/retrieval/results/%s/%s' % (entityName, retrievalExperimentResults)

        # Get the URLs & baseline & PR data for each result
        urls = getResultsUrlsFromRetrievalFile(resultsFilePath, extensions)
        incompleteResults = getExtensionsResultsFromRetrievalFile(resultsFilePath, extensions)

        # Gather the scored results from the index
        scoredResults[entityId] = scoreResults(entity, entityId, urls, features, incompleteResults)

        # Either learn or rank
        if not learn:

            # Create the ranking object & run the training stage with entity data we have now
            rankSVMRanking = RankSVMRanking(scoredResults, relevance, features)

            # Get the ranked results
            results = rankSVMRanking.rank(scoredResults, entityId)

            # Output the ranking results
            outputTitle = "Results Summary (for top %d results):\n"
            outputFile = entityName + '/RankSVMRanking'
            outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results)

    if learn:

        # Create the ranking object & rank
        rankSVMRanking = RankSVMRanking(scoredResults, relevance, features)

        # Learn the ranking model
        rankSVMRanking.learn()
