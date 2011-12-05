from json import dumps, loads
import threading
import cherrypy
import os
from search.SearchThread import SearchThread

__author__ = 'jon'

# Index of queries to maps, where each map holds the status of the current search, and (eventually) the result data of the search
queryResults = {}


class Search(object):
    """
      Provides a web interface to search
    """

    @cherrypy.expose
    def index(self):
        """
          Just return the static HTML content
        """
        return open(os.path.join(RESOURCES_DIR, u'search.html')).read()

    
    @cherrypy.expose
    def search(self, query=None, idField=None):
        """
          Takes in a query, and triggers a search, returning only the status that it has started the query. This will
            add the query into the global data structure and launch the search thread.
        """

        # Get the entity id
        entity = loads(query)
        entityId = entity[idField]

        # Add the new data structure
        global queryResults
        queryResults[query] = {
            'status' : 'Started query...',
            'entity'  : entity,
            'entityId' : entityId,
            'trigger'   : threading.Semaphore()
        }

        # Prepare the response results
        trigger = queryResults[query]['trigger']
        del queryResults[query]['trigger']
        responseString = dumps(queryResults[query])
        queryResults[query]['trigger'] = trigger

        # Start the search thread
        searchThread = SearchThread(queryResults[query])
        searchThread.start()

        # Send back the status of the search (remove non-serializable elements)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return responseString


    @cherrypy.expose
    def update(self, query=None):
        """
          Returns the status of the query as soon as there is an update. Only returns an object with 'status' "done" when
            there will be no more updates.
        """

        # Get the data for this query
        global queryResults
        queryData = queryResults[query]

        # Lock on the query data until it's ready
        queryData['trigger'].acquire()

        # Prepare the response results
        trigger = queryData['trigger']
        del queryData['trigger']
        responseString = dumps(queryData)
        queryData['trigger'] = trigger

        # Send back the status of the search
        print "Responding " + responseString
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return responseString


    
# Server configuration
RESOURCES_DIR = os.path.join(os.path.abspath("."), u"resources")
SCRIPTS_DIR = os.path.join(os.path.abspath("."), u"scripts")
config = {'/resources':
            {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': RESOURCES_DIR,
            },
          '/scripts':
            {
                  'tools.staticdir.on': True,
                  'tools.staticdir.dir': SCRIPTS_DIR,
            }
        }

# Start the server
cherrypy.tree.mount(Search(), '/', config=config)
cherrypy.engine.start()