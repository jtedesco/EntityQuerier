from json import load, loads
import os
from pprint import pprint
import subprocess
import sys
from src.ranking.learning.BM25SpyRanking import BM25SpyRanking
from src.search.extension.BaselineScoreExtension import BaselineScoreExtension
from src.search.extension.ExpandedYQLKeywordExtension import ExpandedYQLKeywordExtension
from src.search.extension.PageRankExtension import PageRankExtension
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from util.GoogleResultsBuilder import buildGoogleResultsFromURLs
from util.RankingExperimentUtil import outputRankingResults

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

        # Train the learning algorithm using the search results & relevance data given
        self.train()


    def buildRankSVMRankingInput(self, qid, rankSVMData, scoredResult, relevantURLs = {}):
        """
          Helps build the string for an entity given a scored search result

            @param  qid             The id number of the query
            @param  rankSVMData     The data generated so far
            @param  scoredResult    The scored search result
            @param  relevantURLs    The relevance set of urls (empty if unknown)
        """

        # The RankSVM relevance label
        preferenceScore = 1
        if str(scoredResult['url']) in relevantURLs:
            preferenceScore = 2

        # build the training line
        rankSVMData += "%d qid:%d" % (preferenceScore, qid)
        for index in xrange(0, len(self.features)):
            feature = self.features[index]

            try:
                if type(scoredResult[feature]) == type(0):
                    rankSVMData += " %d:%d" % (index + 1, scoredResult[feature])
                elif type(scoredResult[feature]) == type(0.0):
                    rankSVMData += " %d:%1.2f" % (index + 1, scoredResult[feature])
                else:
                    print "Unrecognized feature type, feature: " + str(scoredResult[feature])
            except KeyError:
                print "missing feature for %s" % scoredResult['url']
                rankSVMData += " %d:%d" % (index + 1, 0)

        rankSVMData += '   #%s \n' % scoredResult['url']
        return rankSVMData


    def train(self):
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

            for searchResult in self.searchResults[entityId]:
                rankSVMTrainingData = self.buildRankSVMRankingInput(qid, rankSVMTrainingData, searchResult, relevantURLs)

            qid +=1

        # Dump the data to the training file
        trainingDataPath = 'trainingData'
        if os.path.exists(trainingDataPath):
            os.remove(trainingDataPath)
        open(trainingDataPath, 'w').write(rankSVMTrainingData)

        # Remove training file
        if os.path.exists(RankSVMRanking.trainingFilePath):
            os.remove(RankSVMRanking.trainingFilePath)

        # Train RankSVM
        subprocess.Popen([RankSVMRanking.rankSVMPath + 'svm_rank_learn', '-c', '3', trainingDataPath,
                          RankSVMRanking.trainingFilePath]).communicate()
        


    def rank(self, scoredResults, entityId):
        """
          Rank the scored results of a single entity
        """

        # The test input
        testInputPath = 'testInput'
        if os.path.exists(testInputPath):
            os.remove(testInputPath)

        # Build the formatted input data
        rankSVMInputData = "# Entity '%s'\n" % entityId
        for searchResult in scoredResults:
            rankSVMInputData = self.buildRankSVMRankingInput(0, rankSVMInputData, searchResult)
        open(testInputPath, 'w').write(rankSVMInputData)

        # The test output
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


def getDmozResults():

    # Find where we expect this data to be cached
    dmozPath = str(os.getcwd())
    dmozPath = dmozPath[:dmozPath.find('EntityQuerier') + len('EntityQuerier')] + '/dmoz/'

    # Supplement the index with the DMOZ documents
    dmozResults = []
    for filename in os.listdir(dmozPath):

        try:

            # Get the contents of the file
            dmozResultFile = open(dmozPath + filename)
            dmozResult = load(dmozResultFile)
            dmozResults.append(dmozResult)

        except ValueError:

            # Do something awful...
            try:
                dmozResult = eval(dmozResultFile.read())
                dmozResults.append(dmozResult)
            except Exception:
                pass

    # Create the index with both the traditional and new DMOZ search results
    return dmozResults


def buildResultsForEntity(resultsFilePath, verbose, extensions):

    # Get the contents of the file
    resultsData = open(resultsFilePath).read()

    # Strip off the header
    dataToBeJoined = []
    recordData = False
    for dataLine in resultsData.split('\n'):
        if not recordData and len(dataLine) > 0 and dataLine[0] == '{':
            recordData = True
        if recordData:
            dataToBeJoined.append(dataLine)
    resultsData = '\n'.join(dataToBeJoined)

    resultsDump = loads(resultsData)

    # Initialize the extensions (HACK)
    for extension in extensions:
        if 'initialize' in dir(extension):
            extension.initialize(resultsDump)

    # Build the data structure that will map entity id -> urls
    entityUrls = set([])
    for query in resultsDump:
        for resultType in resultsDump[query]:
            for url in resultsDump[query][resultType]:
                if url not in ['precision', 'recall', 'averagePrecision']:
                    entityUrls.add(url)

    # Gather the results
    if not os.path.exists('.index-' + entityId):
        results = buildGoogleResultsFromURLs(entityUrls, verbose=verbose, extensions=extensions)
        print "Gathered all results"
    else:
        results = None

    return results


def scoreResults(entity, entityId, results, features):
    """
      Score the results for an entity

        @param  entity      The entity instance for which to score results
        @param  entityId    The id of the entity instance whose results to score
        @param  results     The unscored results
    """

    # Get a ranking object to allow us to score
    spyRanking = BM25SpyRanking(results, getKeywords(entity), entityId)
    spyRanking.entityId = entityId

    # The data structure in which we're going to store the scored results (scores instead of content)
    scoredResults = {}

    # Get the scores for each feature of this entity
    for feature in features:

        # Check if the feature is already a numeric
        if feature not in {'baselineScore', 'pageRank'}:

            # Run the scoring algorithm on the results
            spyRanking.feature = feature
            spyRanking.rank()

            # Gather the scores
            featureScores = spyRanking.getScores()
            for url in featureScores:
                if url not in scoredResults:
                    numerics = spyRanking.getNumerics()
                    scoredResults[url] = {
                        'url' : url,
                        'baselineScore' : numerics['baselineScore'][url],
                        'pageRank' : numerics['pageRank'][url]
                    }
                scoredResults[url][feature] = featureScores[url]

        else:

            # Copy numeric features
            if results is not None:
                for result in results:
                    url = result['url']
                    try:
                        scoredResults[url][feature] = result[feature]
                    except KeyError:
                        print "Error processing %s, skipping because %s" % (url, str(sys.exc_info()[1]))

    return scoredResults.values()




def getKeywords(entity):

    keywords = []
    for key in entity:
        keywords.extend(key.split())
        if type(entity[key]) == type([]):
            for keyword in entity[key]:
                if keyword is not None:
                    lowercaseKeyword = keyword.lower()
                    if len(lowercaseKeyword.split()) > 1:
                        keywords.append(lowercaseKeyword)
                        keywords.extend(lowercaseKeyword.split())
                    else:
                        keywords.append(lowercaseKeyword)
        else:
            keyword = entity[key]
            if keyword is not None:
                lowercaseKeyword = keyword.lower()
                if len(lowercaseKeyword.split()) > 1:
                    keywords.append(lowercaseKeyword)
                    keywords.extend(lowercaseKeyword.split())
                else:
                    keywords.append(lowercaseKeyword)

    return keywords


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

    # Get the DMOZ results for all entities
    print "getting DMOZ results"
    dmozResults = getDmozResults()
    print "%d dmoz results" % len(dmozResults)

    # Build the relevance sets for each
    retrievalExperimentResults = 'ExactAttributeNamesAndValues'
    resultScores = {}
    relevance = {}
    for entityId in entityIds:

        # Get the entity
        entity = load(open(projectRoot + '/entities/%s.json' % entityId))
        relevance[entityId] = load(open(projectRoot + '/relevanceStandard/%s.json' % entityId))

        # The extensions for results
        extensions = [
            PageRankExtension(),
            YQLKeywordExtension(),
            ExpandedYQLKeywordExtension(),
            BaselineScoreExtension()
        ]

        # Get the retrieval results for this entity
        entityName = entityId.replace(' ', '').replace('-', '')
        resultsFilePath = projectRoot + '/experiments/retrieval/results/%s/%s' % (entityName, retrievalExperimentResults)
        entityResults = buildResultsForEntity(resultsFilePath, True, extensions)
        if entityResults is not None:
            entityResults.extend(dmozResults)
        resultScores[entityId] = scoreResults(entity, entityId, entityResults, features)


    # Create the ranking object & run the training stage with entity data we have now
    rankSVMRanking = RankSVMRanking(resultScores, relevance, features)

    # Run the ranking for each entity
    for entityId in entityIds:

        # Get the entity
        entity = load(open(projectRoot + '/entities/%s.json' % entityId))
        relevantResults = load(open(projectRoot + '/relevanceStandard/' + entityId + '.json'))

        # The extensions for results
        extensions = [
            PageRankExtension(),
            YQLKeywordExtension(),
            ExpandedYQLKeywordExtension(),
            BaselineScoreExtension()
        ]

        # Get the retrieval results for this entity
        entityName = entityId.replace(' ', '').replace('-', '')
        resultsFilePath = projectRoot + '/experiments/retrieval/results/%s/%s' % (entityName, retrievalExperimentResults)
        entityResults = buildResultsForEntity(resultsFilePath, True, extensions)
        resultScores = scoreResults(entity, entityId, entityResults, features)

        # Get the ranked results
        results = rankSVMRanking.rank(resultScores, entityId)

        # Output the ranking results
        outputTitle = "Results Summary (for top %d results):\n"
        outputFile = entityName + '/RankSVMRanking'
        outputRankingResults(entityId, outputFile, outputTitle, projectRoot, results)
