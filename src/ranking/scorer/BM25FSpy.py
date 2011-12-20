from whoosh.scoring import BM25F

class BM25FSpy(BM25F):
    """
      Collects a dictionary of the urls seen -> scores accumulated to
    """

    use_final = True

    @staticmethod
    def initialize():

        BM25FSpy.scores = {}
        BM25FSpy.numerics = {
            'baselineScore' : {},
            'pageRank' : {}
        }

        
    def final(self, searcher, docnum, score):
        """
          Returns the adjusted score (modified using the document's pagerank score)
        """

        # Store the score
        url = searcher.stored_fields(docnum)['url']
        BM25FSpy.scores[url] = score
        BM25FSpy.numerics['baselineScore'][url] = searcher.stored_fields(docnum)['baselineScore']
        try:
             pageRank = searcher.stored_fields(docnum)['pagerank']
        except KeyError:
            pageRank  = 0
        BM25FSpy.numerics['pageRank'][url] = pageRank

        # Record the document we found
        data = "{\n"
        data += '\turl: \'' + str(searcher.stored_fields(docnum)['url']) + '\'\n'
        data += '\tcontent: \'... (' + str(len(searcher.stored_fields(docnum)['content'])) + ' items)\n'
        data += '\ttitle: \'' + str(searcher.stored_fields(docnum)['title']) + '\'\n'
        data += '\theaders: \'' + str(searcher.stored_fields(docnum)['headers']) + '\'\n'
        data += '\tkeywords: \'' + str(searcher.stored_fields(docnum)['keywords']) + '\'\n'
        data += '\tdescription: \'' + str(searcher.stored_fields(docnum)['description']) + '\'\n'
        data += '\tyqlKeywords: \'' + str(searcher.stored_fields(docnum)['yqlKeywords']) + '\'\n'
        data += '\texpandedYqlKeywords: \'' + str(searcher.stored_fields(docnum)['expandedYqlKeywords']) + '\'\n'
        data += '\tpageRank: \'' + str(pageRank) + '\'\n'
        data += '\tbaseline: \'' + str(searcher.stored_fields(docnum)['baselineScore']) + '\'\n'
        data += '}\n\n'
        with open('log', 'a') as f: f.write(data)

        return score
