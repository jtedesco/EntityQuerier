import sys
from src.search.Search import Search
from BeautifulSoup import BeautifulSoup
from src.search.SearchResultParsing import getPageContent
from src.search.google.GoogleResultParserThread import GoogleResultParserThread

__author__ = 'jon'


class GoogleSearch(Search):
    """
      Implements the facade with which to query a specific search engine about the retrieved results
    """

    def query(self, query, numberOfResults=10, fetchContent=True):
        """
          Query the search interface and return a dictionary of results

            @param  query               The query to submit to Google
            @param  numberOfResults     The number of top results to retrieve. This is specifically the number of results
                                            to retrieve, excluding binary binary files if told to skip them
            @param  fetchContent        Determines whether or not we should fill in information about each result's content

            @return A dictionary representing the search results
        """

        # Start on the first page of results
        google_query = str(self.__prepareGoogleQuery(query))
        url = "http://google.com/search?q=" + google_query

        # Parse the content of the results page
        results = []
        while len(results) < numberOfResults and url is not None:

            try:
                # Get the HTML content of the (next) results page
                searchPage = getPageContent(url)

                # Add the results from this page
                newResults, nextPageUrl = self.__parseResults(searchPage, fetchContent)
                results.extend(newResults)
                url = nextPageUrl

            except Exception:

                print "Error querying Google: '%s'" % str(sys.exc_info()[1])

        # Trim the results down to the exact size we want
        results = results[:numberOfResults]

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
                results: A dictionary, parsed from the results, that contains the basic result information
                nextURL: The URL of the next page of results
        """

        results = []

        # Get the result entries (the list of results)
        parsedHTML = BeautifulSoup(resultsContent)
        resultEntries = parsedHTML.findAll('li', {'class' : 'g'})

        # Add entries, and content for each
        nextURL = None
        for resultEntry in resultEntries:

            try:
                
                # Extract all the data we can for this result from the main results page
                url = str(resultEntry.find('a').attrs[0][1])
                preview = resultEntry.find('span', {'class' : 'st'}).text.encode('ascii', 'ignore').lower()

                # Add it to our results
                results.append({
                    'url' : url,
                    'preview' : preview
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

                # Parse the next page's URL from the current results page, if it can be found
                try:
                    nextURL = "http://www.google.com" + str(parsedHTML.find(id='pnnext').attrMap['href'])
                except AttributeError:
                    nextURL = None

            except Exception:

                print "Error parsing basic results data from Google: '%s'" % str(sys.exc_info()[1])

        return results, nextURL


    def __prepareGoogleQuery(self, query):
        """
          Cleans up a query string before submission to Google

            @param  query   The query to clean
            @return The 'cleaned' query
        """

        query = query.replace('+', '%2B')
        query = query.replace(' ', '+')

        return query

