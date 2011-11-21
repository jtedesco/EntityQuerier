import re
import subprocess
from src.search.extension.Extension import Extension

__author__ = 'jon'

class ExpandedYQLKeywordExtension(Extension):

    def getExpandedKeywordsFromKeywords(self, keywords):
        """
            Expand the list of YQL keywords using synonyms from WordNet
        """

        # The template WordNet command
        wordNetArgumentTemplate = "%s -synsa -synsv -synsn"

        # Collect the expanded list of keywords
        expandedKeywords = list(keywords)
        keywordsSet = set(keywords)
        for keyword in keywords:

            errors = "NONE!"
            try:
                # Call WordNet & get output
                arguments = (wordNetArgumentTemplate % keyword).split()
                p = subprocess.Popen(['wn'] + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, errors = p.communicate()

                # Parse WordNet output
                lines = [line.strip() for line in output.split('\n')]
                for i in xrange(0, len(lines)):

                    # If we've reached a new sense
                    if len(lines[i]) > 0 and lines[i].startswith("Sense"):

                        # Find all the synonym keywords
                        for synonym in lines[i+1].split(', '):

                            # Replace parenthesis stuff, and only add it if it's not the same as the original keyword
                            parenthesisRegex = re.compile('\(.*?\)')
                            realSynonym = re.sub(parenthesisRegex, '', synonym).strip()
                            if realSynonym not in keywordsSet:

                                # Keep track of the synonyms we've found
                                expandedKeywords.append(realSynonym)
                                keywordsSet.add(synonym)

            except Exception:
                print "Error getting synonyms from WordNet: '%s'" % errors


        return expandedKeywords


    def run(self, resultDictionary):
        resultDictionary['expandedYqlKeywords'] = self.getExpandedKeywordsFromKeywords(resultDictionary['yqlKeywords'])