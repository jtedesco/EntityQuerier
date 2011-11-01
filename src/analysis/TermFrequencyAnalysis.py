from BeautifulSoup import BeautifulSoup
from json import loads
import os
from pprint import pprint
import re
import operator

__author__ = 'jon'

class TermFrequencyAnalysis(object):
    """
      This class is responsible for providing text-based analyses of the results of a search, regardless of the search
        engine from which the results were retrieved.
    """

    def __init__(self, data):
        """
          Construct an analysis using the search results given, and an optional training set for smooth the term
            frequencies.

            @param  data    the results retrieved from the search interface, which contains a set of documents
        """

        self.data = data
        self.termFrequencyIndex = None
        self.termFrequencyInvertedIndex = None
        self.wordCount = None
        self.cleanResults()

        # Generate the word index (maps url -> terms and term frequencies)
        self.__buildTermFrequencyIndex()

        # Generate the inverted index (maps term -> url and term frequency)
        self.__buildTermFrequencyInvertedIndex()


    def refresh(self):
        """
          Rebuild the term frequency index and inverted index.
        """

        self.termFrequencyIndex = None
        self.termFrequencyInvertedIndex = None

        self.__buildTermFrequencyIndex()
        self.__buildTermFrequencyInvertedIndex()


    def __buildTermFrequencyIndex(self):
        """
          Builds the term frequency index for the given results. The TF index will be constructed at <code>self.termFrequencyIndex</code>
            and will look like this:

                {
                    <url> : (totalWordCount, {
                       <term> : <count>
                        ...
                    })
                    ...
                }
        """

        # Only build this term frequency index 
        if self.termFrequencyIndex is None:
            self.termFrequencyIndex = {}

            for result in self.data:

                terms = result['cleanContent'].split()

                documentTermFrequencyIndex = {}

                for term in terms:
                    if term not in documentTermFrequencyIndex:
                        documentTermFrequencyIndex[term] = 1
                    else:
                        documentTermFrequencyIndex[term] += 1

                url = result['url']
                self.termFrequencyIndex[url] = (len(terms), documentTermFrequencyIndex)


    def __buildTermFrequencyInvertedIndex(self):
        """
          Builds the inverted index for the given results. The inverted index will be constructed at <code>self.termFrequencyInvertedIndex</code>,
            and will look like this:

                {
                    <term> : (totalWordCount, {
                        <url> : <documentCount>
                        ...
                    })
                }
        """

        if self.termFrequencyInvertedIndex is None:
            
            if self.termFrequencyIndex is None:
                self.__buildTermFrequencyIndex()

            self.termFrequencyInvertedIndex = {}
            for url in self.termFrequencyIndex:

                documentTermFrequencyIndex = self.termFrequencyIndex[url][1] # Grab the term index, not document length

                for term in documentTermFrequencyIndex:
                    if term not in self.termFrequencyInvertedIndex:
                        self.termFrequencyInvertedIndex[term] = (documentTermFrequencyIndex[term], {
                            url : documentTermFrequencyIndex[term]
                        })
                    else:

                        # Update total counts
                        count = self.termFrequencyInvertedIndex[term][0]
                        count += documentTermFrequencyIndex[term]

                        # Update document specifics
                        references = self.termFrequencyInvertedIndex[term][1]
                        references[url] = documentTermFrequencyIndex[term]
                        
                        self.termFrequencyInvertedIndex[term] = (count, references)

                        
    def getTotalWordCount(self, url = None):
        """
          Gets the number of total words in a document or in the collection

            @param  url     Optional parameter specifying the document in which to find the word count. If it is not provided,
                            the word count of the collection will be returned
        """

        if url is None or url not in self.termFrequencyIndex:

            # Find the total word count of the collection if it doesn't already exist
            if self.wordCount is None:
                self.wordCount = 0
                for url in self.termFrequencyIndex:
                    self.wordCount += self.termFrequencyIndex[url][0]

            return self.wordCount

        else:

            return self.termFrequencyIndex[url][0]


    def getWordCount(self, term, url = None):
        """
          Gets the number of times the word (term) occurs in a given document or the collection of documents.

            @param  term    The word for which to find the frequency
            @param  url     Optional parameter specifying the document in which to determine the frequency, if
                            it is not provided, the word frequency in the collection will be returned

        """

        wordCount = 0
        if url is None:
            if term in self.termFrequencyInvertedIndex:
                wordCount = self.termFrequencyInvertedIndex[term][0]
        else:
            if term in self.termFrequencyIndex[url][1]:
                wordCount = self.termFrequencyIndex[url][1][term]

        return wordCount
    

    def getWordScore(self, term, url = None):
        """
          Gets the (unsmoothed) p(w|d) for a given term and a web page, calculated using simple (word count / document length)

            @param  term    The term, the score of which we will determine
            @param  url     The document in which to find the term's score (if it is not provided, it will be in the whole collection)
        """

        wordCount = self.getWordCount(term, url)
        totalWordCount = self.getTotalWordCount(url)

        return float(wordCount) / totalWordCount


    def cleanResults(self):
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

        # Clean each result
        cleanData = []
        for result in self.data:

            try:
                originalContent = result['content']

                # Extract <script> tags
                soup = BeautifulSoup(originalContent.lower())
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

                # Add the clean content field in, and move it over the cleaned data
                result['cleanContent'] = cleanContent
                cleanData.append(result)

            except KeyError:
                print "Skipping text analysis of '%s'" % result['url']

        self.data = cleanData


    def getTopKWords(self, k = 10):
        """
          Get the list of most frequent words in this collection

            @param  k   The number of top words to get
        """

        # Sort the dictionary by value
        sortedWords = sorted(self.termFrequencyInvertedIndex.iteritems(), key=operator.itemgetter(1), reverse=True)

        # Get the top k words
        topWords = []
        for i in xrange(0, k):
            try:
                topWords.append(sortedWords[i][0])
            except Exception:
                pass

        return topWords


        
