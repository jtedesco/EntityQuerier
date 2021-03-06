import threading
from urllib2 import URLError
import sys
from src.search.SearchResultParsing import parseMetaDataFromContent, isHTML, getPageContent, parseHeaderInformationFromContent

__author__ = 'jon'

class ResultParserThread(threading.Thread):

    
    def __init__(self, resultDictionary, verbose=False, extensions=[]):
        """
          Initialize this parser, given the dictionary into which the page's data is going to be placed
        """
        threading.Thread.__init__(self)
        self.verbose = verbose
        self.resultDictionary = resultDictionary
        self.url = resultDictionary['url']
        self.extensions = extensions

        
    def run(self):
        """
          Parse the content of this page, and update the given dictionary for this thread
        """

        try:
            # Get the content from this page
            if self.verbose:
                print "Getting page content for '%s'" % self.url.strip()
                
            content = getPageContent(self.url)

            # Verify that this is not binary data
            if content is not None and isHTML(content):


                # Extract basic data about this result
                content = content.lower()
                title, keywords, description = parseMetaDataFromContent(content)
                headers = parseHeaderInformationFromContent(content)

                # Add this result data
                self.resultDictionary['title'] = title
                self.resultDictionary['keywords'] = keywords
                self.resultDictionary['description'] = description
                self.resultDictionary['content'] = content
                self.resultDictionary['headers'] = headers

                # Run the extensions
                for extension in self.extensions:
                    extension.run(self.resultDictionary)


        except URLError:

            # Skip this URL, and register it as an error on the cache
            if self.verbose:
                print("Error accessing '%s', %s" % (self.url.strip(), str(sys.exc_info()[1]).strip()))
