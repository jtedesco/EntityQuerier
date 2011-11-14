from BeautifulSoup import BeautifulSoup
from json import loads
import os
from pprint import pprint
import re
from src.search.SearchResultParsing import loadFromUrl
from util.YQLCache import YQLCache

__author__ = 'jon'

class YQLKeywordWrapper(object):
    
    def __init__(self):

        # The template information for querying the Yahoo keyword service
        self.apiUrl = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20search.termextract%20where%20context%3D%22####%22&format=json'
        self.contentSize = 5000

        # Cache the data retrieved
        self.cache = YQLCache()


    def getKeywordsFromContent(self, content):
        """
          Retrieve the Yahoo keywords from some content, by splitting the content and joining
            the results if the content is too long to be sent via a URL.

            @param  content The content from which to retrieve the keyword information.
        """

        # Split the content
        content = self.__cleanResults(content)
        contentChunks = self.__group(content, self.contentSize)

        # Get the keywords for each chunk
        keywords = set([])
        for chunk in contentChunks:

            # Fill the URL template
            url = self.apiUrl.replace('####', chunk)
            url = url.replace(' ', '%20')

            # Get the keyword data, from the cache if possible
            keywordJson = self.cache.read(url)
            if keywordJson is None:
                keywordJson = loadFromUrl(url)
                self.cache.write(url, keywordJson)
            keywordData = loads(keywordJson)
            fetchedKeywords = keywordData['query']['results'].values()
            
            keywords = keywords.union(set(fetchedKeywords[0]))

        return list(keywords)


    def __cleanResults(self, content):
        """
          Cleans out HTML tags from content of results for this analysis. Results will appear as this after calling
            this method:

            [
                {
                    'url': <url>
                    'preview' : <preview snippet>
                    'title' : <title>
                    'description' : <meta description>
                    'pageRank' : <PageRank, between 0 and 10>
                    'content' : <page content>
                    'cleanContent' : <cleaned page content>
                },
                ...
            ]
        """

        # Remove stop words from the cleaned content
        stopWordsListPath = str(os.getcwd())
        stopWordsListPath = stopWordsListPath[:stopWordsListPath.find('EntityQuerier') + len('EntityQuerier')]
        stopWordsListPath += "/src/analysis/StopWordList.json"
        stopWords = set(loads(open(stopWordsListPath).read()))

        # Extract <script> tags
        soup = BeautifulSoup(content.lower())
        to_extract = soup.findAll('script')
        for item in to_extract:
            item.extract()

        # Extract <style> tags
        to_extract = soup.findAll('style')
        for item in to_extract:
            item.extract()

        # Extract all other tags
        cleanContent = ' '.join(soup.findAll(text=True))

        # Add spaces for HTML spaces
        cleanContent = cleanContent.replace('&nbsp;', ' ')

        # Replace stop words & links
        cleanWords = []
        words = cleanContent.split()
        for word in words:
            if word not in stopWords and 'http' not in word:
                charRegex = re.compile('[^a-zA-Z]')
                nonChars = charRegex.findall(word)
                if len(nonChars) == 0:
                    cleanWords.append(word)
        cleanContent = ' '.join(cleanWords)


        return cleanContent


    def __group(self, content, groupSize):
        return [content[i : i + groupSize] for i in xrange(0, len(content), groupSize)]