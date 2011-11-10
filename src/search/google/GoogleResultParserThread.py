from BeautifulSoup import BeautifulSoup
import os
import subprocess
import threading
from urllib2 import HTTPError, URLError
import sys
from src.search.SearchResultParsing import parseMetaDataFromContent, isHTML, getPageContent

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

        # Find the absolute path to the script to get the pagerank of a page
        pageRankScriptPath = str(os.getcwd())
        pageRankScriptPath = pageRankScriptPath[:pageRankScriptPath.find('EntityQuerier') + len('EntityQuerier')]
        pageRankScriptPath += "/src/search/google/GetPageRank.py"
        self.pageRankScriptPath = pageRankScriptPath

        
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
                pageRank = self.__getPageRank(self.url)

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


    def __getPageRank(self, url):
        """
          Retrieves the approximate PageRank of a given url, as an integer between 0 and 10.

            @param  url The url for which to find the PageRank
            @return An integer representing the PageRank
        """

        try:
            # Go to the pagerank page, enter this url, and hit 'submit' using Twill
            pageRankHTML = subprocess.check_output(["python", self.pageRankScriptPath, url])
            pageRankHTML = pageRankHTML[pageRankHTML.find('==DATA==')+len('==DATA=='):].strip()

            # Parse the output
            parsedPageRankData = BeautifulSoup(pageRankHTML)
            pageRankElementText = parsedPageRankData.find('ul', {'class' : 'prlist'}).text
            try:

                if pageRankElementText[1] == '1':
                    pageRank = int(pageRankElementText[0:2])
                else:
                    pageRank = int(pageRankElementText[0])

            except ValueError:

                # Try to extract the domain this time
                url = url.lstrip('http://')
                domain = url[:url.find('/')]

                # Go to the pagerank page, enter this url, and hit 'submit' using Twill
                pageRankHTML = subprocess.check_output(["python", self.pageRankScriptPath, domain])
                pageRankHTML = pageRankHTML[pageRankHTML.find('==DATA==')+len('==DATA=='):].strip()

                # Parse the output
                parsedPageRankData = BeautifulSoup(pageRankHTML)
                pageRankElementText = parsedPageRankData.find('ul', {'class' : 'prlist'}).text

                try:

                    if pageRankElementText[1] == '1':
                        pageRank = int(pageRankElementText[0:2])
                    else:
                        pageRank = int(pageRankElementText[0])

                except ValueError:
                    pageRank = 0

        except Exception:
            pageRank = 0

        return pageRank