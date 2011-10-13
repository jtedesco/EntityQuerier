import subprocess
from urllib2 import HTTPError
from src.engines.SearchInterface import SearchInterface
from BeautifulSoup import BeautifulSoup

__author__ = 'jon'


class GoogleSearchInterface(SearchInterface):
    """
      Implements the facade with which to query a specific search engine about the retrieved results
    """

    def query(self, query, numberOfResults=10):
        """
          Query the search interface and return a dictionary of results

            @param  query               The query to submit to Google
            @param  numberOfResults     The number of top results to retrieve. This is specifically the number of results
                                            to retrieve, excluding binary binary files if told to skip them

            @return A dictionary representing the search results
        """

        # Start on the first page of results
        url = "http://google.com/search?q=" + self.__prepareQuery(query)

        # Parse the content of the results page
        results = []
        while len(results) < numberOfResults:

            # Get the HTML content of the (next) results page
            searchPage = self.getPageContent(url)

            # Add the results from this page
            newResults, nextPageUrl = self.__parseResults(searchPage)
            results.extend(newResults)
            url = nextPageUrl

        # Trim the results down to the exact size we want
        results = results[:numberOfResults]

        return results


    def __parseResults(self, resultsContent):
        """
          Parse the results from the HTML content of Google's results page

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
        for resultEntry in resultEntries:

            # Get the URL of the page
            url = str(resultEntry.find('a').attrs[0][1])

            try:
                # Get the content from this page
                content = self.getPageContent(url).lower()

                # Verify that this is binary data
                if self.isHTML(content):

                    # Extract data about this result
                    preview = resultEntry.find('span', {'class' : 'st'}).text.encode('ascii', 'ignore').lower()
                    title, keywords, description = self.parseMetaDataFromContent(content)
                    pageRank = self.__getPageRank(url)

                    # Add this result
                    if url not in results:

                        results.append({
                            'url' : url,
                            'title' : title,
                            'keywords' : keywords,
                            'description' : description,
                            'preview' : preview,
                            'pageRank' : pageRank,
                            'content' : '...'
                        })

                    else:
                        print("Found duplicate result entry!")
                else:
                    print("Skipping binary file '%s'" % url)

            except HTTPError:
                
                # Skip this element
                print("Error accessing '%s', skipping" % url)


        nextURL = "http://www.google.com" + str(parsedHTML.find(id='pnnext').attrMap['href'])
        return results, nextURL


    def __prepareQuery(self, query):
        """
          Cleans up a query string before submission to Google

            @param  query   The query to clean
            @return The 'cleaned' query
        """

        query = query.replace('+', '%2B')
        query = query.replace(' ', '+')

        return query


    def __getPageRank(self, url):
        """
          Retrieves the approximate PageRank of a given url, as an integer between 0 and 10.

            @param  url The url for which to find the PageRank
            @return An integer representing the PageRank
        """

        # Go to the pagerank page, enter this url, and hit 'submit' using Twill
        pageRankHTML = subprocess.check_output(["python", "src/engines/GetPageRank.py", url])
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
            pageRankHTML = subprocess.check_output(["python", "src/engines/GetPageRank.py", domain])
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

                # Default to 0 (minimum pagerank)
                pageRank = 0

        return pageRank

