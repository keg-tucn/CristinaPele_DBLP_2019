# pentru text preprocessing
from collections import Counter # pentru gasirea partii de vorbire a unui cuvant (lemmatizare)
from nltk.stem import WordNetLemmatizer # pentru lemmatizare
from nltk.corpus import wordnet # pentru gasirea partii de vorbire a unui cuvant (lemmatizare)

import string
import re
import gensim # stopwords

from helpers import *
###
### Aplica lower pe cuvintele dintr-o lista de documente si elimina punctuatia dintr-o lista de cuvinte.
### param word_list: lista de cuvinte.
### return new_word_list: lista de cuvinte dupa eliminarea punctuatiei.
### param log_step: numarul de iteratii dupa care sa se faca afisare.
###
def elimina_punctuatia(doc_list, log_step = 0):
    new_doc_list = []
    step = 0
    for doc in doc_list:
        if log_step != 0:
            if step % log_step == 0:
                print(step)
            step += 1
        current_word = ""
        new_doc = []
        doc = doc.lower() 
        doc = re.sub(r'\d+', '', doc) # elimina cifrele din document
        for ch in doc:
            if ch == ' ' or ch =='-':
                new_doc.append(current_word)
                current_word = ""
            else:
                if ch not in string.punctuation:
                    current_word += ch
                    
        new_doc.append(current_word)
        new_doc_list.append(new_doc)
        
    return new_doc_list

###
### Elimina stop_words si cuvinte ce nu au lungimea > 2 dintr-o lista de documente.
### param doc_list: lista de documente.
### param log_step: numarul de iteratii dupa care sa se faca afisare.
### return new_doc_list: lista_de_documente dupa eliminarea stop_words si cuvinte cu lungime <=2.
###
def elimina_stopwords(doc_list, log_step=0):
    new_doc_list = []
    step = 0
    for doc in doc_list:
        if log_step != 0:
            if step % log_step == 0:
                print(step)
            step += 1
        new_doc = []
        for word in doc:
            if word not in gensim.parsing.preprocessing.STOPWORDS and len(word) > 2:
                new_doc.append(word)
        new_doc_list.append(new_doc)
    return new_doc_list

###
### Folosit pentru a gasi partea de vorbire a unui cuvant, utila la lemmarizare.
### param word: cuvantul pentru care se doreste gasirea partii de vorbire.
### return n -> noun, v -> verb, a -> adverb.
###

def get_pos( word ):
    w_synsets = wordnet.synsets(word)

    pos_counts = Counter()
    pos_counts["n"] = len(  [ item for item in w_synsets if item.pos()=="n"]  )
    pos_counts["v"] = len(  [ item for item in w_synsets if item.pos()=="v"]  )
    pos_counts["a"] = len(  [ item for item in w_synsets if item.pos()=="a"]  )
    pos_counts["r"] = len(  [ item for item in w_synsets if item.pos()=="r"]  )
    
    most_common_pos_list = pos_counts.most_common(3)
    return most_common_pos_list[0][0]

###
### Lemmatizarea unui cuvant in functie de partea de vorbire a acestuia.
### param word: cuvantul.
### pos: partea de vorbire a cuvantului (optional, default "" si se apeleaza get_pos).
### return cuvantul dupa lemmatizare.
###
def lemmatize_word(word):
    wnl = WordNetLemmatizer()
    return (wnl.lemmatize( word, get_pos(word) ))
    
###
### Aplica lemmatizare pe o lista de documente.
### param doc_list: lista de documente.
### param log_step: numarul de iteratii dupa care sa se faca afisare,
### return lista de documente dupa lemmatizare.
###
def lemmatize(doc_list, log_step = 0):
    new_doc_list = []
    step = 0
    for doc in doc_list:
        if log_step != 0:
            if step % log_step == 0:
                print(step)
            step += 1
        new_doc = []
        for word in doc:
            new_doc.append(lemmatize_word(word))
        new_doc_list.append(new_doc)
    return new_doc_list

###
### Calculeaza dictionar de aparitii {cuvant:nr_aparitii} pentru cuvintele dintr-o lista de documente.
### param doc_list: lista de documente.
### param log_step: numarul de iteratii dupa care sa se faca afisare.
### param ap_dict: dictionarul in care sa se acumuleze rezultatele.
### return ap_dict: dictionarul de aparitii.
###
def calculeaza_dict_aparitii(doc_list, ap_dict = {}, log_step = 0):
    step = 0
    for doc in doc_list:
        if log_step != 0:
            if step % log_step == 0:
                print(step)
            step += 1
        for word in doc:
            try:
                ap_dict[word]+=1;
            except:
                ap_dict[word]=1
    return ap_dict

###
### Dintr-o lista de documente elimina cuvintele a caror aparitie nu se incadreaza in intervalul [min_a,max_a].
### param doc_list: lista de documente.
### param word_dict: dictionarul de aparitii al cuvintelor.
### param min_a: numarul de aparitii minim al unui cuvant.
### param max_a: numarul de aparitii maxim al unui cuvant.
### param log_step: numarul de iteratii dupa care sa se faca afisare.
### return lista de documente dupa eliminarea cuvintelor si eliminarea documentelor goale.
###
def elimina_aparitii(doc_list,word_dict, min_a, max_a, log_step = 0):
    new_doc_list = []
    step = 0
    for doc in doc_list:
        if log_step != 0:
            if step % log_step == 0:
                print(step)
            step += 1
        new_doc = []
        for word in doc:
            if word_dict[word] >= min_a and word_dict[word] <= max_a:
                new_doc.append(word)
        new_doc_list.append(new_doc)
    # elimina doc goale
    return eliminate_empty_lists(new_doc_list)