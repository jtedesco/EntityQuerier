import re
import sys
from src.search.ResultParserThread import ResultParserThread
from BeautifulSoup import BeautifulSoup
from src.search.SearchFacade import SearchFacade
from src.search.SearchResultParsing import getPageContent

__author__ = 'jon'


class GoogleSearchFacade(SearchFacade):
    """
      Implements the facade with which to query a specific search engine about the retrieved results
    """

    def query(self, query):
        """
          Query the search interface and return a dictionary of results
            @param  query   The query to submit to Google
            @return A dictionary representing the search results
        """

        # Start on the first page of results
        googleQuery = str(self.__prepareGoogleQuery(query))
        url = "http://google.com/search?q=" + googleQuery

        if self.verbose:
            print "Querying '%s'..." % query.strip()

        # Parse the content of the results page
        results = []
        while len(results) < self.numberOfResultsToRetrieve and url is not None:
            try:
                # Get the HTML content of the (next) results page
                searchPage = getPageContent(url, True)

                # Add the results from this page
                newResults, nextPageUrl = self.__parseResults(searchPage, fetchContent)
                results.extend(newResults)
                url = nextPageUrl

            except Exception:

                if self.verbose:
                    print "Error querying Google: '%s'" % str(sys.exc_info()[1]).strip()

        # Trim the results down to the exact size we want
        results = results[:self.numberOfResultsToRetrieve]

        return results


    def __parseResults(self, resultsContent, fetchContent):
        """
          Parse the results from the HTML content of Google's results page

          The data structure returned, the first returned value holds data as:
          [
            {
                'url': <url>
                'preview' : <preview snippet>
                'title' : <title>
                'description' : <meta description>
                'pageRank' : <PageRank, between 0 and 10>
                'content' : <page content>
            },
            ...
          ]

            @param  resultsContent The HTML content to parse (the results page of Google)
            @return
                results:    A dictionary, parsed from the results, that contains the basic result information
                nextURL:    The URL of the next page
        """

        results = []

        # Get the result entries (the list of results)
        parsedHTML = BeautifulSoup(resultsContent)
        resultEntries = parsedHTML.findAll('li', {'class' : 'g'})

        try:
            nextLinks = parsedHTML.findAll('a', {'href' : re.compile('^/search'), 'id':'pnnext'})
            nextURL = nextLinks[0].attrMap['href']
            if 'http://' not in nextURL:
                nextURL = 'http://www.google.com' + nextURL
        except Exception, e:
            try:
                otherNextURLTag = parsedHTML.findAll('a', {'href': re.compile('^/search')})[-1]
                if otherNextURLTag.text == 'Next':
                    nextURL = otherNextURLTag.attrMap['href']
                if 'http://' not in nextURL:
                    nextURL = 'http://www.google.com' + nextURL
            except Exception:
                nextURL = None
                print "Failed to find next page URL: %s" % str(e)


        # Add entries, and content for each
        for resultEntry in resultEntries:

            # Extract all the data we can for this result from the main results page
            url = str(resultEntry.find('a').attrs[0][1])

            try:
                preview = resultEntry.find('span', {'class' : 'st'}).text.encode('ascii', 'ignore').lower()
            except AttributeError:
                preview = ""


            # Add it to our results
            result = {
                'url': url,
                'preview': preview
            }
            results.append(result)


        if fetchContent:
            try:
                # Create threads to process the pages for this set of results
                threads = []
                for resultData in results:
                    url = resultData['url']
                    dotLocation = url.rfind('.')
                    if dotLocation != -1 or url[dotLocation:] not in {'.ps', '.pdf', '.ppt', '.pptx', '.doc', 'docx'}:
                        parserThread = ResultParserThread(resultData, self.verbose, self.extensions)
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


            except Exception:

                if self.verbose:
                    print "Error parsing basic results from Google: '%s'" % str(sys.exc_info()[1]).strip()

        return results, nextURL


    def __prepareGoogleQuery(self, query):
        """
          Cleans up a query string before submission to Google

            @param  query   The query to clean
            @return The 'cleaned' query
        """

        query = query.replace('+', '%2B')
        query = query.replace(' ', '+')
        query = query.replace('~', '%7E')

        return query

