import gensim.models.word2vec as w2v
import multiprocessing
import pickle


# Load the preprocessed text as a list of sentences for word2vec training
with open('../data/processed_corpus.pkl', 'rb') as f:
	sentences = pickle.load(f)
f.close()

# Create the word2vec vocabulary
num_of_features = 300
min_word_count = 3
num_of_workers = multiprocessing.cpu_count()
context_size = 7
downsampling = 1e-3
seed = 1

cancer2vec = w2v.Word2Vec(sg = 1,
						 seed = seed,
						 workers = num_of_workers,
						 size = num_of_features,
						 min_count = min_word_count,
						 window = context_size,
						 sample = downsampling)

cancer2vec.build_vocab(sentences)

# Train and save the model
cancer2vec.train(sentences, total_examples = cancer2vec.corpus_count, epochs = cancer2vec.iter)
cancer2vec.save('../data/cancer2vec.w2v')