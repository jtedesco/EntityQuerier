from src.queries.builders.QueryBuilder import QueryBuilder

__author__ = 'jon'


class ApproximateAttributeValuesQueryBuilder(QueryBuilder):
    """
      Builds a query by making a query for every facet of an entity
    """

    def buildQueries(self, entity, idField = 'name'):
        """
          Builds the queries for the given entity, starting with the given id field.

            @param  entity  The entity, given as a dictionary, for which to generate queries
            @param  idField The field that uniquely identifies this entity
        """

        entityIdQuery = "%s" % str(entity[idField])
        queries = [entityIdQuery]

        # Generate queries for each data entry
        for property in entity:
            if property is not idField:

                # Get the property
                entityProperty = entity[property]
                if entityProperty is not None:

                    # Generate a query for each entry in a list
                    if type(entityProperty) == type([]):
                        for property in entityProperty:
                            propertyQuery = str(property)
                            propertyQuery = '~' + ' ~'.join(propertyQuery.split())
                            queries.append(entityIdQuery + ' ' + propertyQuery)
                    elif entityProperty is not None:
                        propertyQuery = str(entityProperty)
                        propertyQuery = '~' + ' ~'.join(propertyQuery.split())
                        queries.append(entityIdQuery + ' ' + propertyQuery)

        return queries
