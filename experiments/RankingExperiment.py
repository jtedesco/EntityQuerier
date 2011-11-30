from json import loads
import os
from src.ranking.BM25Ranking import BM25Ranking
from util.GoogleResultsBuilder import buildGoogleResultsFromURLs

__author__ = 'jon'


class RankingExperiment(object):
    """
      Rank search results
    """

    def __init__(self, resultsFilePath, entity, rankingScheme = BM25Ranking, extensions = [], includeOriginalResults = False, verbose = False):

        if not os.path.exists(rankingScheme.getIndexLocation()):

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

            # Load the data dumped from the first stage
            self.resultsDump = loads(resultsData)

            # Initialize the extensions (HACK)
            for extension in extensions:
                if 'initialize' in dir(extension):
                    extension.initialize(self.resultsDump)

            # Build the data structure that will map entity id -> urls
            self.results = []
            for entityId in self.resultsDump:
                entityUrls = set([])
                for query in self.resultsDump[entityId]:
                    for resultType in self.resultsDump[entityId][query]:
                        for url in self.resultsDump[entityId][query][resultType]:
                            if url not in ['precision', 'recall', 'averagePrecision']:
                                entityUrls.add(url)

                # Assume we're only doing this for one entity
                self.results = buildGoogleResultsFromURLs(entityUrls, True, verbose, extensions)
            print "Retrieved all results from web!"

        else:
            self.results = []
            self.resultsDump = []

        # Get the keywords & build the ranking scheme
        keywords = self.getKeywords(entity)
        if includeOriginalResults:
            self.rankingScheme = rankingScheme(self.results, keywords, self.resultsDump)
        else:
            self.rankingScheme = rankingScheme(self.results, keywords)
        self.rankingScheme.entity = entity
        self.rankingScheme.entityId = entity['name']

        
    def rank(self):
        """
          Get the ranked results using this ranking scheme
        """

        return self.rankingScheme.rank()


    def getKeywords(self, entity):

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
