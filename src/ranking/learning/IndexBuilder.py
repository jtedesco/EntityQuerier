from copy import deepcopy
import os
from whoosh.analysis import CharsetFilter, StemmingAnalyzer
from whoosh.fields import Schema, NUMERIC, TEXT, ID
from whoosh.index import exists_in, open_dir, create_in
from whoosh.support.charset import accent_map
from src.search.extension.BaselineScoreExtension import BaselineScoreExtension
from src.search.extension.ExpandedYQLKeywordExtension import ExpandedYQLKeywordExtension
from src.search.extension.PageRankExtension import PageRankExtension
from src.search.extension.YQLKeywordExtension import YQLKeywordExtension
from src.util.ResultsBuilderUtility import getDmozResults, getResultsFromEntityId

__author__ = 'jon'


class IndexBuilder(object):
    """
      Builds an index for all entities given (either with our without smoothing)
    """

    def __init__(self, indexLocation, entityIds, retrievalExperiment, extensions, smoothed=False):
        """
          Initializes this index builder, based on the used input parameters

            @param  indexLocation           The location in which to build the index
            @param  entityIds               The list of entity ids for entity data to insert into the index
            @param  retrievalExperiment     The name of the retrieval experiment from which to retrieval results
            @param  extensions              The list of extensions to use to build the results for the entities
            @param  smoothed                Whether or not to smooth the index using DMOZ results
        """

        self.indexLocation = indexLocation
        self.entityIds = entityIds
        self.retrievalExperiment = retrievalExperiment
        self.extensions = extensions
        self.smoothed = smoothed

        # Create the schema for the index & add stemmer & accent map
        analyzer = StemmingAnalyzer() | CharsetFilter(accent_map)
        self.indexSchema = Schema(content=TEXT(analyzer=analyzer, stored=True), title=TEXT(analyzer=analyzer, stored=True),
                                  description=TEXT(analyzer=analyzer, stored=True), url=ID(stored=True, unique=True),
                                  pagerank=NUMERIC(stored=True), keywords=TEXT(stored=True), yqlKeywords=TEXT(stored=True),
                                  expandedYqlKeywords=TEXT(stored=True), headers=TEXT(stored=True), baselineScore=NUMERIC(stored=True))


    def buildIndex(self, incremental=False):
        """
          Attempts to build an index either from scratch or incrementally, following the step by step process to do so.

            @param  incremental     Whether or not this index should be build incrementally
        """

        # Check if we can use this index location
        #   (if we're trying to open it, it should be there, otherwise the directory should not be there)
        pathExists = os.path.exists(self.indexLocation)
        if (incremental and pathExists) or (not pathExists or len(os.listdir(self.indexLocation)) == 0):

            # Open or create the index
            if not incremental:

                # Create & build a new index in this directory
                if not pathExists:
                    os.mkdir(self.indexLocation)
                self.index = create_in(self.indexLocation, self.indexSchema)

            else:

                # Check that it's a valid index, and try to open it
                if exists_in(self.indexLocation):
                    self.index = open_dir(self.indexLocation)
                else:
                    raise Exception("Error updating index: Could not open index at '%s'" % self.indexLocation)

            # Get the writer for the index
            indexWriter = self.index.writer()

            # Build the results for all entities
            results = []
            for entityId in self.entityIds:

                print "Building entity results for " + entityId

                # Gather the results (initializing extensions) from the results file
                entityResults = getResultsFromEntityId(entityId, self.retrievalExperiment, deepcopy(self.extensions))
                results.extend(entityResults)

                print "Built entity results for " + entityId

                # Add the documents to the index
                print "Adding results to index for '%s'..." % entityId
                self.__addResults(results, indexWriter)
                print "Added results to index..."

                # Get a new writer to the index
                indexWriter = self.index.writer()

            print "Built all entity results for '%s'" % entityId

            # Get DMOZ documents if necessary
            if self.smoothed:
                print "Building DMOZ documents"
                smoothingDocuments = getDmozResults()
                results.extend(smoothingDocuments)
                print "Built DMOZ documents"

                # Add the documents to the index
                print "Adding results to smoothing index"
                self.__addResults(results, indexWriter)
                print "Added results to index..."

        else:
            raise Exception("Error building index: '%s' already exists" % self.indexLocation)


    def __addResults(self, results, indexWriter):
        """
          Write the results to the index

            @param  results      The results to write to the index
            @param  indexWriter  The writer to use to write to the index
        """

        # Walk the pages folder for content
        for result in results:

            # Convert text entries to unicode safely
            unicodeContent = self.__getFieldFromResult(result, 'content')
            unicodeTitle = self.__getFieldFromResult(result, 'title')
            unicodeDescription = self.__getFieldFromResult(result, 'description')
            unicodeUrl = self.__getFieldFromResult(result, 'url')

            # Get the unicode text representation of list entries (or things that may be lists) from result
            unicodeHeaders = self.__getListFieldFromResult(result, 'headers')
            unicodeKeywords = self.__getListFieldFromResult(result, 'keywords')
            unicodeYqlKeywords = self.__getListFieldFromResult(result, 'yqlKeywords')
            unicodeExpandedYqlKeywords = self.__getListFieldFromResult(result, 'expandedYqlKeywords')

            # Get the numerical entries of the result
            pageRank = self.__getNumericFieldFromResult(result, 'pageRank')
            baselineScore = self.__getNumericFieldFromResult(result, 'baselineScore')

            # Update the existing document in the index if it exists, or add a new one if it doesn't
            indexWriter.update_document(content=unicodeContent, title=unicodeTitle, description=unicodeDescription,
                             yqlKeywords=unicodeYqlKeywords, expandedYqlKeywords=unicodeExpandedYqlKeywords,
                             pagerank=pageRank, url=unicodeUrl, keywords=unicodeKeywords, headers=unicodeHeaders,
                             baselineScore=baselineScore)

        # Commit the writer's changes to disk
        indexWriter.commit()


    def __getListFieldFromResult(self, result, fieldName):
        """
          Safely get a list field from the result
        """
        
        try:
            data = unicode(result[fieldName], errors='ignore')
        except TypeError:
            try:
                data = unicode(', '.join(result[fieldName]), errors='ignore')
            except TypeError:
                data = ', '.join(result[fieldName])
        except KeyError:
            data = unicode('?', errors='ignore')
            
        return data


    def __getFieldFromResult(self, result, fieldName):
        """
          Safely get a field from the result
        """

        try:
            data = unicode(result[fieldName], errors='ignore')
        except TypeError:
            data = result[fieldName]
        except KeyError:
            data = u'?'
            
        return data


    def __getNumericFieldFromResult(self, result, fieldName):
        """
          Safely get a numeric field from the result
        """

        try:
            data = result[fieldName]
        except KeyError:
            data = 0

        return data


if __name__ == '__main__':

    # Parameters for building the index
    entityIds = [
        "ChengXiang Zhai",
        "Danny Dig",
        "Kevin Chen-Chuan Chang",
        "Paris Smaragdis",
        "Matthew Caesar",
        "Ralph Johnson",
        "Robin Kravets"
    ]
    indexLocation = '/home/jon/.index'
    retrievalExperiment = 'ApproximateExactAttributeNamesAndValues'
    extensions = [
        PageRankExtension(),
        YQLKeywordExtension(),
        ExpandedYQLKeywordExtension(),
        BaselineScoreExtension()
    ]

    # Build the index
    indexBuilder = IndexBuilder(indexLocation, entityIds, retrievalExperiment, extensions, True)
    indexBuilder.buildIndex(True)