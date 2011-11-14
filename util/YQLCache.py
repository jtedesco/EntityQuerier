import os
import hashlib
import threading
from util.Cache import Cache

__author__ = 'jon'


errorLock = threading.Lock()
errorsFilename = '.errors.json'

class YQLCache(Cache):
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
        self.cachePath = self.cachePath[:self.cachePath.find('EntityQuerier') + len('EntityQuerier')] + '/cacheyql/'


    def __encodeCacheFilename(self, url):
        """
          Encode the URL to a filename to be stored in the cache
        """
        hashedUrl = hashlib.sha256(url).hexdigest()
        filename = self.cachePath + hashedUrl
        return filename