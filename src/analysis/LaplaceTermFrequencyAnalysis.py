from src.analysis.TermFrequencyAnalysis import TermFrequencyAnalysis

__author__ = 'jon'


class LaplaceTermFrequencyAnalysis(TermFrequencyAnalysis):
    """
      Implements a Laplace-smoothed term frequency analysis
    """

    def __init__(self, data, trainingData):
        """
          Initialize this term frequency analysis using some training document to perform smoothing

            @param  data            The results retrieved from the search interface, which contains a set of documents
            @param  trainingData    The training data to use for smoothing
        """

        TermFrequencyAnalysis.__init__(self, data)
        
        self.trainingDocumentAnalysis = TermFrequencyAnalysis(trainingData)

        
    def getWordScore(self, term, url = None):
        """
          Gets the smoothed p(w|d) for a given term and a web page, calculated using simple
            (word count + 1 / document length + size of training document)

            @param  term    The term, the score of which we will determine
            @param  url     The document in which to find the term's score. If it is not provided, the score from
                            the entire collection will be found (tuning parameter will not be changed based on this)
        """

        smoothedWordCount = self.getWordCount(term, url) + 1
        return float(smoothedWordCount) / (self.getTotalWordCount(url) + self.trainingDocumentAnalysis.getTotalWordCount())