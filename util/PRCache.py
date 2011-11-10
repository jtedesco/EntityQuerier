from BeautifulSoup import BeautifulSoup
from json import load, dump
import os
import hashlib
import subprocess
import threading
from util.Cache import Cache

__author__ = 'jon'


errorLock = threading.Lock()
errorsFilename = '.errors.json'

class PRCache(Cache):
    """
      Represents an interface to a cache for retrieving the PageRank data
    """

    def __init__(self):
        """
          Initialize this PR cache object
        """

        # Find where we expect this data to be cached
        self.cachePath = str(os.getcwd())
        self.cachePath = self.cachePath[:self.cachePath.find('EntityQuerier') + len('EntityQuerier')] + '/cachepr/'

        # Find the absolute path to the script to get the pagerank of a page
        pageRankScriptPath = str(os.getcwd())
        pageRankScriptPath = pageRankScriptPath[:pageRankScriptPath.find('EntityQuerier') + len('EntityQuerier')]
        pageRankScriptPath += "/src/search/google/GetPageRank.py"
        self.pageRankScriptPath = pageRankScriptPath


    def getPageRank(self, url):
        """
          Retrieves the approximate PageRank of a given url, as an integer between 0 and 10. This will be cached.

            @param  url The url for which to find the PageRank
            @return An integer representing the PageRank
        """

        pageRankData = self.read(url)

        if pageRankData is not None:

            try:
                pageRank = int(pageRankData)
            except:
                pageRank = 0

        else:
            
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

            self.write(url, str(pageRank))

        return pageRank


    def __encodeCacheFilename(self, url):
        """
          Encode the URL to a filename to be stored in the cache
        """
        hashedUrl = hashlib.sha256(url).hexdigest()
        filename = self.cachePath + hashedUrl
        return filename