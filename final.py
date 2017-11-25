from textblob import TextBlob
import nltk
import re
import wikipedia as wiki
import string,sys,os

class Article:
    """Retrieves and analyzes wikipedia articles"""

    def __init__(self, filename):
        with open(filename) as f:
            text=f.read()
        f.close()
        self.sentences=nltk.sent_tokenize(text)
        # self.page = wiki.page(title)
        # self.summary = TextBlob(self.page.summary)

    def generate_trivia_questions(self):
        sentences = self.sentences
        # print sentences
        # del sentences[0]
        trivia_sentences = []
        for sentence in sentences:
            chunked=self.get_chunked_data(sentence)
            gaps=self.create_question(sentence,chunked)
            trivia=self.create_gaps(sentence,gaps)
            if trivia:
                trivia_sentences.append(trivia)
        return trivia_sentences

    def get_chunked_data(self, s):
        tokens = nltk.word_tokenize(s)
        tagged = nltk.pos_tag(tokens)
        # print tagged
        grammar =   """  
                    NUMBER: {<$>*<CD>+<NN>*}
                    LOCATION: {<IN><NNP>|<,|IN><NNP>+} 
                    PROPER: {<NNP|NNPS>+}
                    """       
        chunker = nltk.RegexpParser(grammar)
        chunked = chunker.parse(tagged)
        # chunked=nltk.ne_chunk(tagged)
        # print chunked
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
                gaps.append((orig_phrase,word.label()))
        return gaps

    def create_gaps(self,sentence,gaps):
        for gap in gaps:
            if gap[1]=='LOCATION':
                sentence=string.replace(sentence,gap[0],'where')
            elif gap[1]=='NUMBER':
                sentence=string.replace(sentence,gap[0],'which year')
            elif gap[1]=='PROPER':
                sentence=string.replace(sentence,gap[0],'who')

        # lst = [word[0].upper() + word[1:] for word in sentence.split()]
        sentence=string.replace(sentence,'.','?')
        trivia={}
        trivia['question']=sentence
        trivia['answer']=gaps
        return trivia

if __name__=="__main__":
    filename=sys.argv[1]
    obj=Article(filename)
    questions=obj.generate_trivia_questions()
    for question in questions:
        print "Q.",question['question']
        print "Ans.",question['answer']