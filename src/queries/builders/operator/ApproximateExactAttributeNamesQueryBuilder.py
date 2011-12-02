from src.queries.builders.QueryBuilder import QueryBuilder

__author__ = 'jon'


class ApproximateExactAttributeNamesQueryBuilder(QueryBuilder):
    """
      Builds a query by making a query for every facet of an entity
    """

    def buildQueries(self, entity, idField = 'name'):
        """
          Builds the queries for the given entity, starting with the given id field.

            @param  entity  The entity, given as a dictionary, for which to generate queries
            @param  idField The field that uniquely identifies this entity
        """
        
        entityId = str(entity[idField])
        entityIdQuery = '~"%s"' % entityId
        queries = [entityIdQuery]

        # Generate queries for each data entry
        for property in entity:
            if property is not idField:
                propertyQuery = '~"' + str(property) + '"'
                queries.append(entityIdQuery + ' ' + propertyQuery)

        return queries
