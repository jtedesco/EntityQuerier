from pprint import pprint
import subprocess
from src.queries.builders.QueryBuilder import QueryBuilder
from src.queries.builders.operator.AttributeNamesQueryBuilder import AttributeNamesQueryBuilder
from src.queries.builders.operator.AttributeValuesQueryBuilder import AttributeValuesQueryBuilder
from src.queries.builders.order.WordNetPolysemyQueryBuilder import WordNetPolysemyQueryBuilder

__author__ = 'jon'


class ApproximateWordNetPolysemyQueryBuilder(QueryBuilder):
    """
      Builds a query by making a query for every facet of an entity, using both names and values of schema
    """

    def __init__(self):

        self.polysemyQueryBuilder = WordNetPolysemyQueryBuilder()


    def buildQueries(self, entity, idField = 'name'):
        """
          Builds the queries for the given entity, starting with the given id field.

            @param  entity  The entity, given as a dictionary, for which to generate queries
            @param  idField The field that uniquely identifies this entity
        """

        # Build the queries
        wordNetQueries = self.polysemyQueryBuilder.buildQueries(entity, idField)

        # Insert approximate operator into queries
        queries = []
        id = wordNetQueries[0]
        for wordNetQuery in wordNetQueries[1:]:
            query = ' ~'.join(wordNetQuery[len(id):].strip().split())
            queries.append(query)

        return [id] + queries