import os
import hashlib
import threading
import sys
from src.search.google.GetPageRank import getPageRank
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

        Cache.__init__(self)

        # Find where we expect this data to be cached
        self.cachePath = str(os.getcwd())
        self.cachePath = self.cachePath[:self.cachePath.find('EntityQuerier') + len('EntityQuerier')] + '/cachepr/'


    def getPageRank(self, url):
        """
          Retrieves the approximate PageRank of a given url, as an integer between 0 and 10. This will be cached.

            @param  url The url for which to find the PageRank
            @return An integer representing the PageRank
        """

        # Try to read it from the cache
        pageRankData = self.read(url)

        if pageRankData is not None:

            try:
                pageRank = int(pageRankData)
            except Exception:
                print "Error parsing cached pageRank: " + str(sys.exc_info()[1])
                pageRank = -1

                # Try to fetch it again if it failed
                try:
                    pageRank = getPageRank(url)
                except Exception:
                    print "Error retrieving pageRank: " + str(sys.exc_info()[1])
                    pageRank = -1

            # Write it to the cache
            self.write(url, str(pageRank))
        else:

            try:
                pageRank = getPageRank(url)
            except Exception:
                print "Error retrieving pageRank: " + str(sys.exc_info()[1])
                pageRank = -1

            # Write it to the cache
            self.write(url, str(pageRank))

        return pageRank


    def __encodeCacheFilename(self, url):
        """
          Encode the URL to a filename to be stored in the cache
        """
        hashedUrl = hashlib.sha256(url).hexdigest()
        filename = self.cachePath + hashedUrl
        return filename