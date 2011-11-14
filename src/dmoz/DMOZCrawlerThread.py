import hashlib
import os
from pprint import pformat
import threading
from urllib2 import URLError
import sys
from src.search.SearchResultParsing import isHTML, loadFromUrl, parseMetaDataFromContent
from util.PRCache import PRCache

__author__ = 'jon'

class DMOZCrawlerThread(threading.Thread):

    
    def __init__(self, resultDictionary, saveData):

        threading.Thread.__init__(self)

        self.resultDictionary = resultDictionary
        self.url = resultDictionary['url']

        # Find where we expect this data to be cached
        self.savePath = str(os.getcwd())
        self.savePath = self.savePath[:self.savePath.find('EntityQuerier') + len('EntityQuerier')] + '/dmoz/'

        # Whether or not we should be saving the data to disk
        self.saveData = saveData

        # A cache for computing PR
        self.prCache = PRCache()


        
    def run(self):
        """
          Parse the content of this page, and update the given dictionary for this thread
        """

        try:

            # Get the content from this page
            print "Getting page content for '%s'" % self.url.strip()

            filename = self.__encodeCacheFilename(self.url)

            try:
                content = loadFromUrl(self.url)
            except ValueError:
                content = None
                print "Error with URL: " + self.url

            # Extract the content from this page
            if content is not None and isHTML(content):

                # Get the information about this url
                content = content.lower()
                if self.saveData:
                    title, keywords, description = parseMetaDataFromContent(content)
                    pageRank = self.prCache.getPageRank(self.url)

                self.resultDictionary['content'] = content

                
                if self.saveData:

                    # Store the extra data
                    self.resultDictionary['keywords'] = keywords
                    self.resultDictionary['description'] = description
                    self.resultDictionary['pageRank'] = pageRank
                    self.resultDictionary['title'] = title

                    # Save the result file
                    open(filename, 'w').write(pformat(self.resultDictionary))


        except URLError:
            print("Error accessing '%s', %s" % (self.url.strip(), str(sys.exc_info()[1]).strip()))


    def __encodeCacheFilename(self, url):
        """
          Encode the URL to a filename to be stored in the cache
        """
        try:
            hashedUrl = hashlib.sha256(url).hexdigest()
        except UnicodeDecodeError:
            hashedUrl = hashlib.sha256(url.decode(errors='ignore')).hexdigest()
        filename = self.savePath + hashedUrl
        return filename