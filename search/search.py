from json import dumps
from time import sleep
import cherrypy
import os

__author__ = 'jon'

# Indexed by queries, and
queryResults = {}

iterations = 0

class Search(object):
    """
      Provides a web interface to search
    """

    @cherrypy.expose
    def index(self):
        return open(os.path.join(RESOURCES_DIR, u'search.html')).read()

    @cherrypy.expose
    def search(self, query=None):
        """
          Takes in a query, and triggers a search, returning only the status that it has started the query
        """

        global iterations
        iterations = 0
        
        print "started"

        cherrypy.response.headers['Content-Type'] = 'application/json'
        return dumps({"status": "Started query..."})


    @cherrypy.expose
    def update(self, query=None):
        """
          Returns the status of the query as soon as there is an update. Only returns an object with 'status' "done" when
            there will be no more updates.
        """

        sleep(1)

        print "iterating"

        global iterations
        if iterations < 5:

            iterations += 1
            
            cherrypy.response.headers['Content-Type'] = 'application/json'
            return dumps({'status': "Update number " + str(iterations)})

        else:

            cherrypy.response.headers['Content-Type'] = 'application/json'
            return dumps({'hello' : 'world', 'status':'done'})





def search(query):
    """
      Actually performs the search
    """


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

cherrypy.tree.mount(Search(), '/', config=config)
cherrypy.engine.start()