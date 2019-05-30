import operator # folosit la sortarea dictionarelor

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
    new_list = []
    for elem in list_:
        if elem not in new_list:
            new_list.append(elem)
    return new_list


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