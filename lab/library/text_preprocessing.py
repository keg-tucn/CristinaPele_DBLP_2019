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
###
def elimina_punctuatia(doc_list):
    new_doc_list = []
    for doc in doc_list:
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
### return new_doc_list: lista_de_documente dupa eliminarea stop_words si cuvinte cu lungime <=2.
###

def elimina_stopwords(doc_list):
    new_doc_list = []
    for doc in doc_list:
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
### return lista de documente dupa lemmatizare.
###
def lemmatize(doc_list):
    new_doc_list = []
    for doc in doc_list:
        new_doc = []
        for word in doc:
            new_doc.append(lemmatize_word(word))
        new_doc_list.append(new_doc)
    return new_doc_list

###
### Calculeaza dictionar de aparitii {cuvant:nr_aparitii} pentru cuvintele dintr-o lista de documente.
### param doc_list: lista de documente.
### return ap_dict: dictionarul de aparitii.
###
def calculeaza_dict_aparitii(doc_list):
    ap_dict = {}
    for doc in doc_list:
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
### return lista de documente dupa eliminarea cuvintelor si eliminarea documentelor goale.
###
def elimina_aparitii(doc_list,word_dict, min_a, max_a):
    new_doc_list = []
    for doc in doc_list:
        new_doc = []
        for word in doc:
            if word_dict[word] >= min_a and word_dict[word] <= max_a:
                new_doc.append(word)
        new_doc_list.append(new_doc)
    # elimina doc goale
    return eliminate_empty_lists(new_doc_list)

###
### Calculeaza df pentru un camp dintr-un set de fisiere.
### param cale: calea spre setul de fisiere.
### param range_: numarul de fisiere.
### param camp: campul pentru care se va calcula df.
### return df: dictionar {cuvant, valoare_df} 
###
def calculeaza_df(cale, range_, camp):
    df = {}
    for i in range(0,range_):
        fisier_citire = cale + str(i) + '.txt'
        r = open(fisier_citire,'r')
        
        for linie in r:
            df_paper = []
            articol_curent = json.loads(linie)
            crt_df =remove_duplicates(articol_curent[camp])
            for elem in crt_df:
                try:
                    df[elem] += 1
                except:
                    df[elem] = 1   
        r.close()
    return df


###
### Calculeaza idf pentru un camp dintr-un set de fisiere.
### param cale: calea spre setul de fisiere.
### param range_: numarul de fisiere.
### param n: numarul de articole din fisiere.
### param df: dictionar document frequency pentru cuvintele din camp(daca este {}, se calculeaza).
### param camp: campul pentru care se doreste calcularea idf(default "", daca df este {}. este obligatorie valarea campului).
### return df: dictionarul rezultat {cuvant:valoare_idf}
###
def calculeaza_idf(cale, range_, n, df = {}, camp = ""):
    if len(df) == 0:
        df = calculeaza_df(cale, range_, camp)
    for elem in df:
        df[elem] = n / df[elem]
    return df


###
### Calculeaza tf_idf pentru un set de fisiere si pune rezultatele tot in fisiere.
### param cale_in: calea spre fiserele de intrare.
### param cale_out: calea spre fisierele de iesire.
### param range_: numarul de fisiere de intrare.
### param idf_dict: dictionar {cuvant:valoare_idf}.
### param camp: campul din datele din fisier pentru care se va calcula tf_idf.
###
def calculeaza_tf_idf(cale_in, cale_out, range_, idf_dict, camp):
    for i in range(0, range_):
        fisier_in = cale_in + str(i) + '.txt'
        fisier_out = cale_out + str(i) + '.txt'
        r = open(fisier_in,'r')
        w = open(fisier_out,'w')
        for linie in r:
            tf = {}
            articol_curent = json.loads(linie)
            camp_curent = articol_curent[camp]
            for cuv in camp_curent:
                try:
                    tf[cuv] += 1
                except:
                    tf[cuv] = 1
                    
            for cuv in tf:
                tf_idf[cuv] = int(tf[cuv] * int(idf_dict[cuv]))
            articol_curent[camp] = tf_idf
            w.write(json.dumps(articol_curent))
            w.write('\n')
            
        w.close()   
        r.close()