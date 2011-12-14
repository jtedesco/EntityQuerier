from math import log
import operator
from src.ranking.Ranking import Ranking

__author__ = 'jon'

class BaselineRanking(Ranking):
    """
      Represents a baseline ranking of the original search results.
    """

    def __init__(self, searchResults, keywords, originalSearchResults):
        """
          Creates a ranking object with the necessary parameters

            @param  searchResults   The list of search results, in the following format:
                                        [
                                            {
                                                'url': <url>
                                                'preview' : <preview snippet>
                                                'title' : <title>
                                                'description' : <meta description>
                                                'pageRank' : <PageRank, between 0 and 10>
                                                'content' : <page content>
                                            },
                                            ...
                                        ]
            @param  keywords        The keywords for these search results to use for scoring the results
            @param  originalSearchResults
                        Will look like this:
                            self.results = {
                                <entity id> :
                                    <query> : {
                                        relevantDocumentsRetrieved : [
                                            ...
                                        ]
                                        nonRelevantDocumentsRetrieved : [
                                            ...
                                        ]
                                        relevantDocumentsNotRetrieved : [
                                            ...
                                        ]
                                        nonRelevantDocumentsNotRetrieved : [
                                            ...
                                        ]
                                        score : <query score>
                                    }

                                    ... (same thing for all queries) ...

                                    overall : {
                                        relevantDocumentsRetrieved : [
                                            ...
                                        ]
                                        nonRelevantDocumentsRetrieved : [
                                            ...
                                        ]
                                        relevantDocumentsNotRetrieved : [
                                            ...
                                        ]
                                        nonRelevantDocumentsNotRetrieved : [
                                            ...
                                        ]
                                        score : <query score>
                                    }
                                ...
                            }
        """

        self.searchResults = searchResults
        self.keywords = keywords
        self.originalSearchResults = originalSearchResults


    def rank(self):
        """
          Perform the ranking, creating the baseline ranking. The scoring scheme is that for each result we find in
            a given query's results:

                score(q_i) = SUM(log(rank_in_query_results(q_i)))

        """

        # Build an index (by url) of these results
        results = {}
        for result in self.searchResults:
            results[result['url']] = result

        # Score the results
        scoredResults = {}
        for entityId in self.originalSearchResults:
            for query in self.originalSearchResults[entityId]:

                rank = 1
                numberOfResults = len(self.originalSearchResults[entityId][query]['documentsRetrieved'])
                for url in self.originalSearchResults[entityId][query]['documentsRetrieved']:

                    rankScore = numberOfResults - rank + 1

                    if url not in scoredResults:
                        scoredResults[url] = (log(rankScore), results[url])
                    else:
                        scoredResults[url] = (scoredResults[url][0] + log(rankScore), scoredResults[url][1])

                    rank += 1

        # Re-rank the urls
        reRankedResults = []
        sortedResults = sorted(scoredResults.iteritems(), key=operator.itemgetter(1), reverse=True)
        for result in sortedResults:
            reRankedResults.append(result[1])

        return reRankedResults
        