from BeautifulSoup import BeautifulSoup
from src.dmoz.DMOZCrawlerThread import DMOZCrawlerThread

__author__ = 'jon'

class DMOZCrawler(object):
    """
      Crawler class that encapsulates the crawler logic. This file is intended to be run once, to fetch as much data from DMOZ as possible.
    """

    def __init__(self):

        # The root DMOZ urls from which to start
        self.urlsToCrawl = [
            'http://www.dmoz.org/Shopping/',
            'http://www.dmoz.org/Reference/',
            'http://www.dmoz.org/Kids_and_Teens/',
            'http://www.dmoz.org/Games/',
            'http://www.dmoz.org/Arts/',
            'http://www.dmoz.org/Society/',
            'http://www.dmoz.org/Regional/',
            'http://www.dmoz.org/News/',
            'http://www.dmoz.org/Health/',
            'http://www.dmoz.org/Business/',
            'http://www.dmoz.org/Sports/',
            'http://www.dmoz.org/Science/',
            'http://www.dmoz.org/Recreation/',
            'http://www.dmoz.org/Home/',
            'http://www.dmoz.org/Computers/'
        ]

        self.urlsCrawled = set([])


    def __getLinksFromPage(self, content):

        # Parse content
        soup = BeautifulSoup(content)
        referenceLists = soup.findAll('ul', {'class' : 'directory dir-col'})
        links = []
        for referenceList in referenceLists:
            linkElements = referenceList.findAll('a')
            for link in linkElements:
                relativeUrl = link.attrs[0][1]
                absoluteUrl = self.__buildAbsoluteLinks([relativeUrl])
                links.extend(absoluteUrl)

        return links


    def __getUrlsFromPage(self, content):

        # Parse content
        soup = BeautifulSoup(content)
        referenceLists = soup.findAll('ul', {'class' : 'directory-url'})
        urls = []
        for referenceList in referenceLists:
            linkElements = referenceList.findAll('a')
            for link in linkElements:
                urls.append(link.attrs[0][1])
                
        return urls


    def __launchThreads(self, crawlData, saveData = False):

        # Create threads to fetch these pages
        threads = []
        for url in crawlData:
            parserThread = DMOZCrawlerThread(crawlData[url], saveData)
            threads.append(parserThread)

        # Launch all threads
        for thread in threads:
            thread.start()

        # Wait for all the threads to finish
        for thread in threads:
            # Allow up to 5 seconds for this thread to respond, otherwise, kill it
            thread.join(5)

            # Kill it if it hung
            if thread.isAlive():
                try:
                    thread._Thread__stop()
                except Exception:
                    print(str(thread.getName()) + ' could not be terminated')


    def __buildAbsoluteLinks(self, links):
        """
          Builds a list of absolute links for a given list of relative links and a parent/root url.
        """

        # Create a new list of absolute links
        absoluteLinks = []

        # Rewrite all of the given links to absolute links
        for link in links:

            # Rewrite relative-absolute links
            if link.startswith('/'):
                link = 'http://www.dmoz.org' + link
                if link not in absoluteLinks:
                    absoluteLinks.append(link)

            # Take care of absolute links
            elif link not in absoluteLinks and link.startswith('http'):
                absoluteLinks.append(link)

        return absoluteLinks


    def run(self):

        while True:

            # Grab the URLs to crawl in this phase
            urlsToCrawl = self.urlsToCrawl
            self.urlsToCrawl = []

            # Create some data structure to hold the crawl data
            crawlData = {}
            for url in urlsToCrawl:
                crawlData[url] = {
                    'url' : url
                }

            # Launch threads to fetch all of this data in parallel
            self.__launchThreads(crawlData)

            # Examine crawled data from this stage, and extract pages to crawl
            urlsFound = set([])
            for url in crawlData:

                # Get the relevant links from this page (to other pages to crawl)
                try:
                    content = crawlData[url]['content']
                    linksFromPage = self.__getLinksFromPage(content)

                    # Add all links from this page that haven't been crawled
                    for linkFromPage in linksFromPage:
                        if linkFromPage not in self.urlsCrawled:
                            self.urlsToCrawl.append(linkFromPage)

                    # Get all web links from this page
                    urlsFromPage = self.__getUrlsFromPage(content)
                    for url in urlsFromPage:
                        if url not in self.urlsCrawled:
                            urlsFound.add(url)
                except KeyError:
                    print "Error getting URL content for '%s': %s" % (url, crawlData[url])

            # Crawl all actual links from the web
            webData = {}
            for url in urlsFound:
                webData[url] = {
                    'url' : url
                }
            self.__launchThreads(webData, True)


            # Record the links we've already crawled
            for url in crawlData:
                self.urlsCrawled.add(url)



if __name__ == '__main__':
    
    crawler = DMOZCrawler()
    crawler.run()

