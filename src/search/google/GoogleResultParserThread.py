from BeautifulSoup import BeautifulSoup
import os
import subprocess
import threading
from urllib2 import HTTPError, URLError
import sys
from src.search.SearchResultParsing import parseMetaDataFromContent, isHTML, getPageContent
from util.PRCache import PRCache

__author__ = 'jon'

class GoogleResultParserThread(threading.Thread):

    
    def __init__(self, resultDictionary, verbose=False):
        """
          Initialize this parser, given the dictionary into which the page's data is going to be placed
        """
        threading.Thread.__init__(self)
        self.verbose = verbose

        self.resultDictionary = resultDictionary
        self.url = resultDictionary['url']

        self.prCache = PRCache()

        
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


                # Extract data about this result
                content = content.lower()
                title, keywords, description = parseMetaDataFromContent(content)
                pageRank = self.prCache.getPageRank(self.url)

                # Add this result data
                self.resultDictionary['title'] = title
                self.resultDictionary['keywords'] = keywords
                self.resultDictionary['description'] = description
                self.resultDictionary['pageRank'] = pageRank
                self.resultDictionary['content'] = content

        except URLError:

            # Skip this URL, and register it as an error on the cache
            if self.verbose:
                print("Error accessing '%s', %s" % (self.url.strip(), str(sys.exc_info()[1]).strip()))
