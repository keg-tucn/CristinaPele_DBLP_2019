import operator # folosit la sortarea dictionarelor
import itertools # folosit la sortarea listelor
from scipy.spatial import distance # folosit la calcularea distantelor intre vectori (calculeaza_distante)

###
### Elimina listele goale dintr-o lista de liste.
### param doc_list: lista de liste.
### return new_doc_list: lista de liste fara liste goale.
###
def eliminate_empty_lists(doc_list):
    new_doc_list = []
    for doc in doc_list:
        if len(doc) > 0 :
            new_doc_list.append(doc)
            
    return new_doc_list



###
### Elimina duplicatele dintr-o lista.
### param list_: lista.
### return lista dupa eliminarea duplicatelor.
###
def remove_duplicates(list_):
    return list(dict.fromkeys(list_))

###
### Elimina duplicate din lista de liste.
### param list_: lista initiala.
### return lista dupa eliminare duplicatelor.
###
def remove_duplicates_lol(list_):
    list_.sort()
    return list(list_ for list_,_ in itertools.groupby(list_))


###
### Returneaza cuvinte unice dintr-un set de documente.
### param doc_list: lista de documente.
### return lista cu cuvinte unice.
###
def get_word_list(doc_list):
    word_list = []
    for doc in doc_list:
        for word in doc:
            word_list.append(word)
    return remove_duplicates(word_list)

###
### Sorteaza un dictionar dupa valoare.
### param dict_: dictionarul ce trebuie sortat.
### return dictionarul dupa sortare.
def sort_dict_value(dict_):
    return sorted(dict_.items(), key=operator.itemgetter(1))

###
### Gaseste valoarea maxima dintr-un dictionar {key:value}.
### param dict_: dictionarul.
### return max_: valoarea maxima din dictionar.
###
def get_max_dict(dict_):
    max_ = -1
    for key in dict_:
        if dict_[key] > max_ :
            max_ = dict_[key]
    return max_


###
### Elimina elementele din dictionar ce nu au valoarea >= min_a si <= max_a.
### param dict_: dictionarul.
### param min_a: valoarea minima.
### param max_a: valoarea maxima.
### return dict_nou: dictionarul dupa eliminare.
###
def eliminare_aparitii_dict(dict_, min_a, max_a):
    dict_nou = {}
    for elem in dict_:
        if dict_[elem] >= min_a and dict_[elem] <= max_a:
            dict_nou[elem] = dict_[elem]
    return dict_nou

###
### Pune cheile dintr-un dictionar intr-o lista.
### param dict_: dictionarul.
### return lista: lista de chei din dictionar.
###
def dict_to_lista(dict_):
    lista = []
    for elem in dict_:
        lista.append(elem)
    return lista


###
### Avand o lista de label de forma [[elem_cls,..,elem_cls],..,[elem_cls]] o transforma in [cls,cls,...,cls].
### param clusters: lista de labels initiala
### return X: vector cu lista de labels finala
###
def get_labels(clusters):
    nr_points = 0
    for c in clusters:
        nr_points += len(c)
    X = np.zeros(nr_points)
    crt_c = 0
    for c in clusters:
        for elem in c:
            X[elem] = crt_c
        crt_c += 1
    return X

###
### Calculeaza numarul de intrari dintr-un set de fisiere.
### param cale: calea spre setul de fisiere.
### param range_: numarul de fisiere.
### return n: numarul de intrari din fisiere.
###
def calculeaza_nr_articole(cale, range_):
    n = 0
    for i in range(0, range_):
        fisier = cale + str(i) + '.txt'
        r = open(fisier,'r')
        for linie in r:
            n += 1
        r.close()
    return n


###
### Sterge elementul cu o anumite cheie din dictionar.
### param d: dictionarul.
### param key: cheia
### return r: un nou dictionar fara elemetul corespunzator cheii specificate.
###
def elimina_elem_dupa_cheie(d, key):
    r = dict(d)
    del r[key]
    return r

###
### Calculeaza distanta dintre un vector si un set de valori (vectori) dintr-un dictionar si returneaza
### primii nr cei mai apropiati vectori.
### param X: vectorul.
### param X_dict: dictionarul.
### param nr: numarul de vectori returnati.
### return distante[0:nr]: primele nr elemente din dictionarul {cheie:vector}
###
def calculeaza_distante(X, X_dict, nr):
    distante = {}
    for elem in X_dict:
        distante[elem] = distance.euclidean(X, X_dict[elem])
    distante = sort_dict_value(distante)
    return distante[0:nr]

###
### Calculeaza distanta euclidiana dintre doi vectori.
### param v1: primul vector.
### param v2: al doilea vector.
### return distanta: distanta dintre vectori.
###
def calculeaza_distanta(v1, v2):
    distanta = distance.euclidean(v1, v2)
    return distanta


###
### Creeaza o lista noua formata din elementele comune a doua liste.
### param l1: lista 1.
### param l2: lista 2.
### return intersectia listelor.
###
def elemente_comune_lista(l1,l2):
    return list(set(l1).intersection(l2))