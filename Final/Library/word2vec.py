from gensim.models import Word2Vec
import gensim.downloader as api
import numpy as np

#https://radimrehurek.com/gensim/models/word2vec.html
#https://github.com/RaRe-Technologies/gensim/blob/3d7293f3831250a47cf8e85a7f493a87c7d6ac32/gensim/models/word2vec.py#L865

# gensim.models.word2vec.Word2Vec(
#    sentences=None,        -> iterable of iterables, list of lists of tokens                             
#    corpus_file=None,      -> path spre corpus
#    size=100,              -> dimensiunea vectorilor de cuvinte
#    alpha=0.025,           -> learning rate initial
#    window=5,              -> distanta maxima dintre cuvantul curent si cel prezis in propozitie
#    min_count=5,           -> ignora cuvintele cu o frecventa mai mica decat asta
#    max_vocab_size=None,   -> limiteaza RAM la dimensiunea asta pt cuvintele unice din dictionar 
#    sample=0.001,          -> treshold pt a selecta caror cuvinte li se face downsampling 
#    seed=1,                -> vectorii initiali sunt word + str(seed)
#    workers=3,             -> nr de threaduri
#    min_alpha=0.0001,      -> learning rate scade liniar pe parcursul trainingului la asta
#    sg=0,                  -> algoritmul de train; 1-> skip-gram, 0-> CBOW
#    hs=0,                  -> 1 se foloseste hierarhical clustering pentru train; 0 se foloseste negative sampling
#    negative=5,            -> pt negative sampling : cate puncte de noise se folosesc
#    ns_exponent=0.75,      -> exponent used to shape the negative sampling distribution
#    cbow_mean=1,           -> 0 : sum of context words, 1 mean -> se aplica doar la cbow
#    hashfxn=<built-in function hash>, 
#    iter=5,                -> nr de epoci 
#    null_word=0,           -> 
#    trim_rule=None, 
#    sorted_vocab=1,        -> sorteaza dictionarul descrescator dupa frecventa inainte sa asigneze vectorii
#    batch_words=10000,     -> nr de cuvinte trimise la un worker
#    compute_loss=False,    -> calculeaza loss
#    callbacks=(),          -> functii care sa fie apelate la anumite momente in train
#    max_final_vocab=None)  -> limiteaza vocabularul dupa min_count

# build_vocab(
#     sentences=None,       -> iterable of iterables, list of lists of tokens                             
#     corpus_file=None,     -> path spre corpus
#     update=False,         -> True: cuvinte noi vor fi adaugate la modelul deja antrnat
#     progress_per=10000,   -> la cate cuvinte sa arate progresul
#     keep_raw_vocab=False, -> se sterge vocabularul raw duoa scalare
#     trim_rule=None, 
#     **kwargs)

# train(
#     sentences=None,       -> iterable of iterables, list of lists of tokens
#     corpus_file=None,     -> path spre corpus
#     total_examples=None,  -> nr de propozitii
#     total_words=None,     -> nr total de cuvinte din dictionar
#     epochs=None,          -> epocile de rulare
#     start_alpha=None,     -> learning rate de start
#     end_alpha=None,       -> learning rate de final
#     word_count=0,         -> nr cuvintelor pe care s-a facut deja antrenarea
#     queue_factor=2,       -> multiplu pentru dimensiunea cozii
#     report_delay=1.0,     -> nr de secunde inainte sa arate un progres
#     compute_loss=False,   -> calculeaza loss -> get_latest_training_loss() da valoarea calculata
#     callbacks=())

###
### Antrenare word2vec.
### param doc_list: lista de documente.
### param model_name: numele sub care sa fie salvat modelul.
### param window: distanta maxima dintre cuvantul curent si cel prezis in propozitie.
### param size: dimensiunea vectorilor.
### param min_count: numarul minim de aparitii pentru un cuvant.
### param workers: numarul de threaduri.
### param iter: numarul de iteratii din antrenare(epoci).
### param hs: 1- foloseste hierarchical clustering, 0 foloseste negative sampling
### return model: modelul antrenat.
###
def train_word2vec(doc_list, model_name, window=1, size=50, min_count=1, workers=8, iter=20, hs=0):
    model = Word2Vec(size=size, window=window, min_count=min_count, workers=workers, iter=iter)
    model.build_vocab(doc_list)
    model.train(doc_list,total_examples=model.corpus_count, epochs=iter)
    model.delete_temporary_training_data(replace_word_vectors_with_normalized=False)
    model_name += '.model'
    model.save(model_name)
    return model


###
### Incarca in memorie un model pre-antrenat.
### param model_path: calea panala model.
### return modelul.
###
def load_model_w2v(model_path):
	return Word2Vec.load(model_path)

###
### Incarca in memorie modelul pre-antrenat glove_wiki_50 (https://github.com/RaRe-Technologies/gensim-data).
### return modelul
###
def load_glove_50():
	return api.load("glove-wiki-gigaword-50")


###
### Incarca in memorie modelul pre-antrenat glove_wiki_100 (https://github.com/RaRe-Technologies/gensim-data).
### return modelul
###
def load_glove_100():
	return api.load("glove-wiki-gigaword-100")


###
### Aplica word2vec pe o lista de documente.
### param doc_list: lista de documente (lista de liste).
### param model: modelul de word2vec antrenat.
### param size: dimensiunea de output a vectorului w2v.
### param func: functia ce se aplica pe vectorii unui document {sum, avg}, default sum.
### return X: lista de np.array(size), fiecare element reprezentand vectorului unui document.
###
def apply_model_w2v(doc_list, model, size, func="sum", print_=False):
	X = {}
	not_found_words = 0
	total_words = 0
	i = 0
	for doc in doc_list:
		if i % 100 == 0:
			print(i)
		i += 1
		X_doc = np.zeros(size)
		words = 0
		key = ""
		for word in doc:
			key += word + ' '
			try:
				embed = model[word]
				words+=1
				for i in range(0,size):
					X_doc[i] += embed[i]
			except:
				if print_ == True:
					print(word)
				not_found_words += 1
		if words > 0:
			X_aux = []
			if func == 'avg':
				for i in range(0,size):
					X_doc[i] /= words
			for elem in X_doc:
				X_aux.append(elem)
			total_words += words
			X[key] = X_aux
	print('Not found ' + str(not_found_words) + ' words from ' + str(total_words) + ' words.')
	return X

###
### Calculeaza perplexity pentru modelul antrenat.
### param model: modelul antrenat.
### return perplexity: 2**train_loss
###
def get_perplexity(model):
	return decimal.Decimal(2)**decimal.Decimal(model.get_latest_training_loss())