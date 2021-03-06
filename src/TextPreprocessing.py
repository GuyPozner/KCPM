from gensim.models.phrases import Phraser, Phrases
import pandas as pd
import pickle
import spacy
from spacy.en import English

# Load a spacy pipline
nlp = spacy.load('en')

# Adding stop words to the spacy vocabulary
stop_words = ['abstract', 'methods', 'discussion', 'results', 'figure', 'fig', 'summary', 'conclusions', 'analysis']
for stop_word in stop_words:
    lexme = nlp.vocab[stop_word]
    lexme.is_stop = True

# Read the texts
train_text = pd.read_csv('../data/training_text', sep = "\|\|", engine = 'python', header=None, skiprows=1, names=["ID","Text"], encoding = 'utf-8')
test_text = pd.read_csv('../data/test_text', sep = '\|\|', engine = 'python', header=None, skiprows=1, names=["ID","Text"], encoding = 'utf-8')


# Combine all the texts into strings as a corpus
def combine_texts(texts):
    raw_corpus = ''
    for text in texts:
        raw_corpus += ' ' + text
    return raw_corpus

raw_corpus = combine_texts(train_text['Text']) + combine_texts(test_text['Text'])

# Clean the corpus
def clean_corpus(raw_corpus):
    annotated_corpus = nlp(raw_corpus)
    sentences = []
    for sentence in annotated_corpus.sents:
        word_list = []
        for word in sentence:
            if not word.is_stop and not word.is_punct and not len(word) > 16 and not word.like_num and not word.is_digit and not word.is_space:
                if word.is_alpha:
                    word_list.append(word.orth_)
        sentences.append(word_list)
    return sentences

text_clean_corpus = clean_corpus(raw_corpus)

# Create bigrams and trigrmas
def create_bigram_and_trigram(sentences):
    bigram = Phrases(sentences, min_count=10, threshold=10, delimiter=b' ')
    bigram_phraser = Phraser(bigram)
    bigramer = bigram_phraser[sentences]
    trigram = Phrases(bigram_phraser[sentences], min_count=10, threshold=10, delimiter=b' ')
    trigram_phraser = Phraser(trigram)
    trigramer = trigram_phraser[bigramer]  
    return trigramer	#the trigamer also include trigrams and bigrams

text_bigram_and_trigram = create_bigram_and_trigram(text_clean_corpus)
processed_corpus = [sentence for sentence in text_bigram_and_trigram]

# Pickle the processed corpus - ready for word2vec training
with open('../data/processed_corpus.pkl', 'wb') as f:
    pickle.dump(processed_corpus, f)



