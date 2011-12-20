from src.queries.builders.QueryBuilder import QueryBuilder
from src.queries.builders.YahooKeywordQueryBuilder import YahooKeywordQueryBuilder
from src.queries.builders.order.WordNetPolysemyQueryBuilder import WordNetPolysemyQueryBuilder

__author__ = 'jon'


class CombinedQueryBuilder(QueryBuilder):
    """
      Builds a query by making a query for every relevant keyword returned from Yahoo for an entity description
    """

    def __init__(self):

        # Get query builders using Yahoo keywords & WordNet
        self.yahooKeywordQueryBuilder = YahooKeywordQueryBuilder()
        self.wordNetQueryBuilder = WordNetPolysemyQueryBuilder()


    def buildQueries(self, entity, idField = 'name'):
        """
          Builds the queries for the given entity, starting with the given id field.

            @param  entity  The entity, given as a dictionary, for which to generate queries
            @param  idField The field that uniquely identifies this entity
        """

        yahooQueries = self.yahooKeywordQueryBuilder.buildQueries(entity, idField)
#        WordNetPolysemyQueryBuilder.numberOfQueries
        orderedYahooQueries = self.wordNetQueryBuilder.orderQueries(entity[idField], yahooQueries)

        return orderedYahooQueries
