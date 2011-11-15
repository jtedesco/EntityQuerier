from json import loads
from pprint import pformat, pprint
import re
from src.ranking.PageRankTermVectorRanking import PageRankTermVectorRanking
from util.GoogleResultsBuilder import buildGoogleResultsFromURLs

__author__ = 'jon'


class RankingExperiment(object):
    """
      Rank search results
    """

    def __init__(self, resultsFilePath, entity, rankingScheme = PageRankTermVectorRanking, extensions = [], includeOriginalResults = False, verbose = False):

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
                    lowercaseKeyword = keyword.lower()
                    if len(lowercaseKeyword.split()) > 1:
                        keywords.append(lowercaseKeyword)
                        keywords.extend(lowercaseKeyword.split())
                    else:
                        keywords.append(lowercaseKeyword)
            else:
                lowercaseKeyword = entity[key].lower()
                if len(lowercaseKeyword.split()) > 1:
                    keywords.append(lowercaseKeyword)
                    keywords.extend(lowercaseKeyword.split())
                else:
                    keywords.append(lowercaseKeyword)

        return keywords
