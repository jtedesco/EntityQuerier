from BeautifulSoup import BeautifulSoup
import re

__author__ = 'jon'

class TermFrequencyAnalysis(object):
    """
      This class is responsible for providing text-based analyses of the results of a search, regardless of the search
        engine from which the results were retrieved.
    """

    def __init__(self, results, trainingSet = None):
        """
          Construct an analysis using the search results given, and an optional training set for smooth the term
            frequencies.
        """

        self.results = results
        self.termFrequencyIndex = None
        self.termFrequencyInvertedIndex = None
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
                    <url> : {
                       <term> : <count>
                        ...
                    }
                    ...
                }
        """

        # Only build this term frequency index 
        if self.termFrequencyIndex is None:
            self.termFrequencyIndex = {}

            for result in self.results:

                terms = result['cleanContent'].split()

                documentTermFrequencyIndex = {}

                for term in terms:
                    if term not in documentTermFrequencyIndex:
                        documentTermFrequencyIndex[term] = 1
                    else:
                        documentTermFrequencyIndex[term] += 1

                self.termFrequencyIndex[result['url']] = documentTermFrequencyIndex


    def __buildTermFrequencyInvertedIndex(self):
        """
          Builds the inverted index for the given results. The inverted index will be constructed at <code>self.termFrequencyInvertedIndex</code>,
            and will look like this:

                {
                    <term> : (totalCount, {
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

                documentTermFrequencyIndex = self.termFrequencyIndex[url]

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

        # Clean each result
        for result in self.results:

            originalContent = result['content']

            # Extract <script> tags
            soup = BeautifulSoup(originalContent.lower())
            to_extract = soup.findAll('script')
            for item in to_extract:
                item.extract()

            # Extract all other tags
            cleanContent = ' '.join(soup.findAll(text=True))
            
            result['cleanContent'] = cleanContent
