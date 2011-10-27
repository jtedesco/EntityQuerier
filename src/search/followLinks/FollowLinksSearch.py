from BeautifulSoup import soup
from src.search.Search import Search
from src.search.google.GoogleResultParserThread import GoogleResultParserThread
from src.search.google.GoogleSearch import GoogleSearch

__author__ = 'jon'

class FollowLinksSearch(Search):
    """
      This class allows us to augment results by retrieving links from the first pages of each query
    """

    def __init__(self, searchScheme = GoogleSearch, numberOfResultsToRetrieve=50, verbose=False, topResultsToFollowLinks=5):
        """
          Initializes this search object
        """

        Search.__init__(numberOfResultsToRetrieve, verbose)
        self.searchScheme = searchScheme
        self.topResultsToFollowLinks = topResultsToFollowLinks


    def query(self, query, fetchContent=True):

        # Get the search results from the 'concrete' scheme
        searchResults = self.searchScheme.query(query, fetchContent)

        resultPages = list(searchResults)

        # Follow the links on the top results
        newResults = []
        for i in xrange(0, self.topResultsToFollowLinks):

            # Find the links from the top results
            theseResults = self.__getResultsFromPageLinks(resultPages[i]['content'], fetchContent)
            newResults.extend(theseResults)


    def __getResultsFromPageLinks(self, content, fetchContent):
        """
          Parse the links from the page content to find these links, using the Google results parser thread

            @param  content The HTML page content from which to grab links
        """
        results = []

        # Extract urls for this page
        parsedContent = soup(content)
        urls = str(parsedContent.findAll('a'))
        descriptions = str(parsedContent.findAll('a'))

        for items in zip(urls, descriptions):

            url = items[0].attrs[0][1]
            description = items[1].attrs[0][0]

            # Add it to our results
            results.append({
                'url' : url,
                'preview' : description
            })
        
        if fetchContent:
            
            # Create threads to process the pages for this set of results
            threads = []
            for resultData in results:
                parserThread = GoogleResultParserThread(resultData)
                threads.append(parserThread)

            # Launch all threads
            for thread in threads:
                thread.start()

            # Wait for all the threads to finish
            for thread in threads:
                thread.join()

        return results

