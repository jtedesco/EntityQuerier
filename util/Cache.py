from json import load, dump
import os
import hashlib
from pprint import pprint
import threading

__author__ = 'jon'


errorLock = threading.Lock()
errorsFilename = '.errors.json'

class Cache(object):
    """
      Represents an interface to the cache, abstracting the details of how files are retrieved or saved.
    """

    def __init__(self):
        """
          Initialize this cache object
        """

        # Find where we expect this data to be cached
        self.cachePath = str(os.getcwd())
        self.cachePath = self.cachePath[:self.cachePath.find('EntityQuerier') + len('EntityQuerier')] + '/cache/'


    def read(self, url):
        """
          Reads some URL from the cache
        """

        # Encode the URL into the filename found in the cache
        filename = self.__encodeCacheFilename(url)

        # Read the data from the cache, if it exists
        if os.path.exists(filename) and os.path.isfile(filename):

            content = open(filename).read()

            if content == "ERROR":
                content = None

        else:
            content = None

        return content


    def write(self, url, content):
        """
          Saves some page to the cache
        """

        # Encode the URL into the filename found in the cache
        filename = self.__encodeCacheFilename(url)

        try:

            cache = open(filename, 'w')
            cache.write(content)
            cache.close()

        except IOError:

            # This frequently happens when the URL is too long to act as a filename, just don't cache it
            print("Error writing to cache! Url: '%s'" % url)


    def registerUrlError(self, url):
        """
          Register that there was an error fetching some URL
        """

        # Lock & read the list of erroneous urls
        errorLock.acquire()
        errorUrls = list(load(open(self.cachePath + errorsFilename)))

        # If this url is not already in the list, add it to the error list and dump it out to file
        if url not in errorUrls:
            errorUrls.append(url)
            dump(errorUrls, open(self.cachePath + errorsFilename, 'w'), indent=4)

        # Allow other threads to register this URL
        errorLock.release()

        # Write a dummy file in the cache for this URL
        filename = self.__encodeCacheFilename(url)
        open(filename, 'w').write("ERROR")


    def __encodeCacheFilename(self, url):
        """
          Encode the URL to a filename to be stored in the cache
        """
        try:
            hashedUrl = hashlib.sha256(url).hexdigest()
        except UnicodeDecodeError:
            hashedUrl = hashlib.sha256(url.decode(errors='ignore')).hexdigest()
        filename = self.cachePath + hashedUrl
        return filename