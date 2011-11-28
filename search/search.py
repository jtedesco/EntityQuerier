from json import dumps
import cherrypy
import os

__author__ = 'jon'

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
          Takes in a query, and triggers a search
        """

        print "Submitting: " + query

        cherrypy.response.headers['Content-Type'] = 'application/json'
        return dumps({"hello" : "world"})



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