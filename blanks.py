from textblob import TextBlob
import nltk
import re
import wikipedia as wiki
import string

class Article:

    def __init__(self, title):
        self.page = wiki.page(title)
        self.summary = TextBlob(self.page.summary)

    def generate_trivia_questions(self):
        sentences = self.summary.sentences
        del sentences[0]
        trivia_sentences = []
        for sentence in sentences:
            chunked=self.get_chunked_data(sentence)
            gaps=self.create_question(sentence,chunked)
            trivia=self.create_gaps(sentence,gaps)
            if trivia:
                trivia_sentences.append(trivia)
        return trivia_sentences

    def get_chunked_data(self, s):
        tokens = s.tokens
        tagged = nltk.pos_tag(tokens)
        grammar =   """  
                    NUMBER: {<$>*<CD>+<NN>*}
                    LOCATION: {<IN><NNP>+<,|IN><NNP>+} 
                    PROPER: {<NNP|NNPS><NNP|NNPS>+}
                    """       
        chunker = nltk.RegexpParser(grammar)
        chunked = chunker.parse(tagged)
        return chunked

    def create_question(self, sentence, chunked):
        gaps = []
        # print chunked
        # print "hello"
        for word in chunked:
            if type(word) != tuple:
                # print word                
                target = []
                for y in word:
                    target.append(y[0])
                    # print y
                orig_phrase = " ".join(target) 
                gaps.append(orig_phrase)
        return gaps

    def create_gaps(self,sentence,gaps):
        for gap in gaps:
            sentence=string.replace(sentence,gap,'_____')
        trivia={}
        trivia['question']=sentence
        trivia['answer']=gaps
        return trivia

if __name__=="__main__":
    obj=Article('Isaac Newton')
    questions=obj.generate_trivia_questions()
    for question in questions:
        print "Q.",question['question']
        print "Ans.",question['answer']
          