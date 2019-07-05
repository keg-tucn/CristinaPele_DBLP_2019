# pentru text preprocessing
from collections import Counter # pentru gasirea partii de vorbire a unui cuvant (lemmatizare)
from nltk.stem import WordNetLemmatizer # pentru lemmatizare
from nltk.corpus import wordnet # pentru gasirea partii de vorbire a unui cuvant (lemmatizare)
from nltk.corpus import brown # pentru verificarea cuvintelor care sunt in engleza

import string
import re
import gensim # stopwords

import json

from helpers import *

###
### Elimina punctuatia si transforma toate litere dintr-o propozitie in litere mici.
### param prop: propozitia.
### return new_prop: propozitia dupa procesare.
###
def elimina_punctuatia_propozitie(prop):
    cuvant_curent = ""
    new_prop = []
    prop = prop.lower() 
    prop = re.sub(r'\d+', '', prop) # elimina cifrele din propozitie
    for ch in prop:
        if ch == ' ' or ch =='-':
            new_prop.append(cuvant_curent)
            cuvant_curent = ""
        else:
            if ch not in string.punctuation:
                cuvant_curent += ch
                    
    new_prop.append(cuvant_curent)
    return new_prop


###
### Aplica lower pe cuvintele dintr-o lista de documente si elimina punctuatia dintr-o lista de cuvinte.
### param doc_list: lista de cuvinte.
### return doc_list_noua: lista de cuvinte dupa eliminarea punctuatiei.
###
def elimina_punctuatia(doc_list, log_step = 0):
    doc_list_noua = []
    step = 0
    for doc in doc_list:
        if log_step != 0:
            if step % log_step == 0:
                print(step)
            step += 1
        cuvant_curent = ""
        doc_nou = []
        doc = doc.lower() 
        doc = re.sub(r'\d+', '', doc) # elimina cifrele din document
        for ch in doc:
            if ch == ' ' or ch =='-':
                doc_nou.append(cuvant_curent)
                cuvant_curent = ""
            else:
                if ch not in string.punctuation:
                    cuvant_curent += ch
                    
        doc_nou.append(cuvant_curent)
        doc_list_noua.append(doc_nou)
        
    return doc_list_noua


###
### Elimina stop_words si cuvinte ce nu au lungimea > 2 dintr-o propozitie (lista de cuvinte).
### param prop: propozitia, lista de cuvinte.
### return prop_nou: lista de cuvinte dupa eliminarea stop_words si cuvinte cu lungime <=2.
###

def elimina_stopwords_propozitie(prop):
    prop_nou = []
    for cuvant in prop:
        if cuvant not in gensim.parsing.preprocessing.STOPWORDS and len(cuvant) > 2:
            prop_nou.append(cuvant)
    return prop_nou

###
### Elimina stop_words si cuvinte ce nu au lungimea > 2 dintr-o lista de documente.
### param doc_list: lista de documente.
### return doc_list_nou: lista_de_documente dupa eliminarea stop_words si cuvinte cu lungime <=2.
###

def elimina_stopwords(doc_list, log_step=0):
    doc_list_nou = []
    step = 0
    for doc in doc_list:
        if log_step != 0:
            if step % log_step == 0:
                print(step)
            step += 1
        doc_nou = []
        for cuvant in doc:
            if cuvant not in gensim.parsing.preprocessing.STOPWORDS and len(cuvant) > 2:
                doc_nou.append(cuvant)
        doc_list_nou.append(new_doc)
    return doc_list_nou

###
### Folosit pentru a gasi partea de vorbire a unui cuvant, utila la lemmarizare.
### param cuvant: cuvantul pentru care se doreste gasirea partii de vorbire.
### return n -> noun, v -> verb, a -> adverb.
###

def get_pos( cuvant ):
    w_synsets = wordnet.synsets(cuvant)

    pos_counts = Counter()
    pos_counts["n"] = len(  [ item for item in w_synsets if item.pos()=="n"]  )
    pos_counts["v"] = len(  [ item for item in w_synsets if item.pos()=="v"]  )
    pos_counts["a"] = len(  [ item for item in w_synsets if item.pos()=="a"]  )
    pos_counts["r"] = len(  [ item for item in w_synsets if item.pos()=="r"]  )
    
    most_common_pos_list = pos_counts.most_common(3)
    return most_common_pos_list[0][0]

###
### Lemmatizarea unui cuvant in functie de partea de vorbire a acestuia.
### param cuvant: cuvantul.
### pos: partea de vorbire a cuvantului (optional, default "" si se apeleaza get_pos).
### return cuvantul dupa lemmatizare.
###
def lemmatize_word(cuvant):
    wnl = WordNetLemmatizer()
    return (wnl.lemmatize( cuvant, get_pos(cuvant) ))
    
###
### Aplica lemmatizare pe o lista de documente.
### param doc_list: lista de documente.
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
### Aplica lemmatizare pe cuvintele unei propozitii (lista de cuvinte).
### param prop: lista de cuvinte reprezentand propozitia.
### return prop_noua: lista de cuvinte dupa aplicarea lemmatizarea.
###
def lemma_propozitie(prop):
    prop_noua = []
    for cuv in prop:
        prop_noua.append(lemmatize_word(cuv))
    return prop_noua

###
### Calculeaza dictionarul de aparitii a cuvintelor dintr-o propozitie(lista de cuvinte).
### param prop: lista de cuvinte.
### param dict_aparitii: dictionarul in care vor fi acumulate aparitiile.
### return dict_aparitii: dictionarul rezultat.
###
def dict_aparitii_propozitie(prop, dict_aparitii):
    for cuvant in prop:
        try:
            dict_aparitii[cuvant] +=1
        except:
            dict_aparitii[cuvant] = 1
    return dict_aparitii

###
### Calculeaza dictionar de aparitii {cuvant:nr_aparitii} pentru cuvintele dintr-o lista de documente.
### param doc_list: lista de documente.
### return ap_dict: dictionarul de aparitii.
###
def calculeaza_dict_aparitii(doc_list, log_step):
    ap_dict = {}
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
### Elimina cuvintele dintr-o propozitie (lista de cuvinte), dupa aparitii.
### param prop: lista de cuvinte.
### param dict_cuvinte: dictionarul de aparitii al cuvintelor {cuv:nr_aparitii}.
### param min_a: numarul minim (inclusiv) de aparitii a unui cuvant.
### param max_a: numarul maxim (inclusiv) de aparitii a unui cuvant.
### return prop_noua: lista de cuvinte dupa eliminarea cuvintelor.
###
def elimina_aparitii_propozitie(prop, dict_cuvinte, min_a, max_a):
    prop_noua = []
    for cuvant in prop:
        if dict_cuvinte[cuvant] >= min_a and dict_cuvinte[cuvant] <= max_a:
            prop_noua.append(cuvant)
    
    return prop_noua

###
### Dintr-o lista de documente elimina cuvintele a caror aparitie nu se incadreaza in intervalul [min_a,max_a].
### param doc_list: lista de documente.
### param word_dict: dictionarul de aparitii al cuvintelor.
### param min_a: numarul de aparitii minim al unui cuvant.
### param max_a: numarul de aparitii maxim al unui cuvant.
### return lista de documente dupa eliminarea cuvintelor si eliminarea documentelor goale.
###
def elimina_aparitii(doc_list,word_dict, min_a, max_a, log_step):
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

###
### Elimina cuvintele care nu sunt in engleza dintr-o propozitie (lista de cuvinte).
### param prop: lista de cuvinte.
### return prop_noua: lista dupa eliminarea cuvintelor.
###
def elimina_cuvintele_nonengl(prop):
    prop_noua = []
    for cuvant in prop:
        if cuvant in brown.words():
            prop_noua.append(cuvant)
    return prop_noua


###
### Elimina cuvinte care nu sunt in engleza dintr-o propozitie.
### param prop: propozitia.
### return prop_noua: propzitia dupa eliminarea cuvintelor in alte limbi.
###
def elimina_non_eng_propozitie(prop):
    prop_noua = []
    
    for cuvant in prop:
        if wordnet.synsets(cuvant):
            prop_noua.append(cuvant)
    return prop_noua



###
### Elimina denumiri de tari si orase dintr-o propozitie.
### param prop: propozitia.
### return prop_noua: propozitia dupa eliminare.
###
def elimina_denumiri_geografice(prop):
	prop_noua = []
	r = open('../Date/Auxiliare/country_list.json')
	lista_tari = json.load(r)
	for cuvant in prop:
		if cuvant not in lista_tari:
			prop_noua.append(cuvant)
	return prop_noua


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
            tf_idf = {}
            for cuv in tf:
                tf_idf[cuv] = int(tf[cuv] * int(idf_dict[cuv]))
            articol_curent[camp] = tf_idf
            w.write(json.dumps(articol_curent))
            w.write('\n')
            
        w.close()   
        r.close()