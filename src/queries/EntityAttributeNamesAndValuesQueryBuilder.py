from src.queries.EntityAttributeNamesQueryBuilder import EntityAttributeNamesQueryBuilder
from src.queries.EntityAttributeValuesQueryBuilder import EntityAttributeValuesQueryBuilder
from src.queries.QueryBuilder import QueryBuilder

__author__ = 'jon'


class EntityAttributeNamesAndValuesQueryBuilder(QueryBuilder):
    """
      Builds a query by making a query for every facet of an entity, using both names and values of schema
    """

    def __init__(self):

        self.entityNamesQueryBuilder = EntityAttributeNamesQueryBuilder()
        self.entityValuesQueryBuilder = EntityAttributeValuesQueryBuilder()


    def buildQueries(self, entity, idField = 'name'):
        """
          Builds the queries for the given entity, starting with the given id field.

            @param  entity  The entity, given as a dictionary, for which to generate queries
            @param  idField The field that uniquely identifies this entity
        """

        queries = self.entityNamesQueryBuilder.buildQueries(entity, idField).append(self.entityValuesQueryBuilder(entity, idField))
        return queries
