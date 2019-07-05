#https://radimrehurek.com/gensim/models/doc2vec.html

import gensim


# gensim.models.doc2vec.Doc2Vec.infer_vector(
# 	doc_words, 			-> lista de string, documentul pentru care se va face inferarea.
# 	alpha=None, 		-> learning rate, daca e nespecificat, se foloseste cel de la initializare.
# 	min_alpha=None, 	-> learning rate va scadea liniar la aceasta valoare.
# 	epochs=None, 		-> numarul de ori de care se va antrena noul document
# 	steps=None)			-> nume vechi pentru epochs.


###
### Incarca un model de doc2vec pre-antrenat.
### param cale_model: calea spre model.
### param alpha: learning rate (defult 0.01).
### param epoci: numarul de epoci (defult 1000).
### return modelul.
###
def load_doc2vec_model(cale_model, alpha=0.01, epoci=1000):
	return gensim.models.Doc2Vec.load(cale_model)


###
### Aplica doc to vec pe un document (lista de string).
### param model: modelul de doc2vec deja antrenat.
### param doc: documentul (lista de string) pe care se va aplica modelul.
### param alpha: learning rate intial (default 0.01)
### param epoci: numarul de ori de care se va face antrenarea (default 1000).
### return vectorul de valori numerice rezultat in urma aplicatii modelului pe document.
###
def aplica_model_d2v(model, doc, alpha=0.01, epoci=1000 ):
	return model.infer_vector(doc,alpha = alpha, epochs = epoci).tolist()