import re
import nltk
import string
import pandas as pds
import heapq
df = pds.read_excel("C:/Users/sravan.kumar.panasa/Documents/POC_Task/amazon_review_summarization/reviews.xlsx")
# list of reviews of 'review' column
reviews_list=df['review'].tolist()
# Getting all reviews as String
reviews_string=' '.join(list(df['review']))
# Removing white spaces
reviews=re.sub(r'\s+',' ',reviews_string)
# Converting to lowercase
#tokenization
#stopwords removal
def preprocess(text):
    lowercasetext=text.lower()
    tokens=[]
    for token in nltk.word_tokenize(lowercasetext):
        tokens.append(token)
    stopwords=nltk.corpus.stopwords.words('english')
    tokens=[word for word in tokens if word not in stopwords and word not in string.punctuation]
    formattedtext=' '.join(word for word in tokens)
    return formattedtext
formattedtext=preprocess(reviews)
#word frequency
word_freq=nltk.FreqDist(nltk.word_tokenize(formattedtext))
highest_freq=max(word_freq.values())
# changing word freq dict with weights
for word in word_freq.keys():
    word_freq[word]=(word_freq[word]/highest_freq)
#sentence tokenization
#sentence_list=nltk.sent_tokenize(reviews)
# instead of sentance list i am taking reviews list
#Sentence Score
score_reviews={}
for review in reviews_list:
    for word in nltk.word_tokenize(review.lower()):
        if review not in score_reviews:
            score_reviews[review]=word_freq[word]
        else:
            score_reviews[review] += word_freq[word]
#summarization
# first parameter 3 means only first top 3 reviews will be displayed in summary
best_reviews=heapq.nlargest(3,score_reviews,key=score_reviews.get)
summary=' '.join(best_reviews)
print(summary)


