from src.analysis.TermFrequencyAnalysis import TermFrequencyAnalysis

__author__ = 'jon'


class DirichletPriorTermFrequencyAnalysis(TermFrequencyAnalysis):
    """
      Implements a Laplace-smoothed term frequency analysis
    """

    def __init__(self, data, trainingData, tuningParameter = 10):
        """
          Initialize this term frequency analysis using some training document to perform smoothing

            @param  data             The results retrieved from the search interface, which contains a set of documents
            @param  trainingData     The data to use for smoothing
            @param  tuningParameter  Parameter to use for the amount of reliance on the training set which represents the
                                       number of 'pseudo-counts' to give to a word that never occurs in the given document
        """

        TermFrequencyAnalysis.__init__(self, data)
        
        self.trainingDocumentAnalysis = TermFrequencyAnalysis(trainingData)
        self.tuningParameter = tuningParameter

        
    def getWordScore(self, term, url = None):
        """
          Gets the smoothed p(w|d) for a given term and a web page, calculated using simple
            (word count + 1 / document length + size of training document)

            @param  term    The term, the score of which we will determine
            @param  url     The document in which to find the term's score. If it is not provided, the score from
                            the entire collection will be found (tuning parameter will not be changed based on this)
        """

        # The smoothed count, updated based on the term score from the training data
        smoothedWordCount = self.getWordCount(term, url) + self.tuningParameter * self.trainingDocumentAnalysis.getWordScore(term)

        return float(smoothedWordCount) / (self.getTotalWordCount(url) + self.tuningParameter)