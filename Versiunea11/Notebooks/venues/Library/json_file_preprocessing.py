import json

###
### Creeaza o lista cu elementele unui field dintr-un fisier json.
### param field: campul din fisier de care este nevoie.
### param file_path: calea spre fisier.
### param unique: impune sau nu unicitatea elementelor din lista (default True).
### param current_list: ista la care vor fi adaugate campurile.
### return current_list: o lista cu toate campurile cerute.
###
def get_field(field, file_path, unique = True, current_list = []):
    r = open(file_path, 'r')
    for line in r:
        crt_line = json.loads(line)
        current_list.append(crt_line[field])
    
    if unique == True:
        current_list = list(dict.fromkeys(current_list))
        
    r.close()
    return current_list

###
### Creeaza o lista din campul unui camp a unui fisier json. Folosit pentru FOS.
### param field_list: lista ce are ca elemente campurile cerute [camp, subcamp al campului].
### param file_path: calea spre fisier.
### param unique: impune sau nu unicitatea elementelor din lista (default True).
### param current_list: lista la care vor fi adaugate subcampurile.
### return current_list: lista cu toate subcampurile campului din fisier.
###
def get_field_of_field(field_list, file_path, current_list = [], unique = True):
    r = open(file_path, 'r')
    for line in r:
        crt_line = json.loads(line)
        crt_line = crt_line[field_list[0]]
        for elem in crt_line:
            current_list.append(elem[field_list[1]])
    
    if unique == True:
        current_list = list(dict.fromkeys(current_list))
    r.close()
    return current_list


###
### Creeaza o lista de string (venue) dintr-un fisier json.
### param filePath: calea spre fisier.
### param current_list: lista in care se vor acumula variabilele string.
### param unique: impune sau nu unicitatea elementelor din lista (default True).
### return current_list: lista de venue.
###
def get_venue_raw_field(filePath, current_list = [], unique = True):
    r = open(filePath, 'r')
    for line in r:
        crt_line = json.loads(line)
        crt_line = crt_line['venue']['raw']
        current_list.append(crt_line)
    
    if unique == True:
        current_list = list(dict.fromkeys(current_list))
    
    r.close()
    return current_list

###
### Creeaza o lista de abstracte (list of docs).
### param file_path: calea spre fisier.
### param current_list: lista la care vor fi adaugate listele cuvintelor din abstractele.
### param unique: impune sau nu unicitatea elementelor din lista (default True).
### return current_list: lista de abstracte (list of docs).
###
def get_indexed_abstract_field(file_path, current_list = [], unique = True):
    r = open(file_path,'r')
    
    for line in r:
        crt_line = json.loads(line)
        crt_abstr = crt_line['indexed_abstract']
        crt_abstr_list = ""
        for elem in crt_abstr:
            crt_abstr_list += elem + ' '
        current_list.append(crt_abstr_list[0:len(crt_abstr_list) - 1])

    if unique == True:
        current_list = list(dict.fromkeys(current_list))
    
    r.close()
    return current_list

###
### Creeaza abstract din indexed_abstract, extrage campurile id, title, authors, venue si fos si scrie in fisiere json rezultatele.
### param read_file_path: fisierul de unde se citesc indexed_abstracts.
### param write_file_path: lista de fisiere de iesire.
###
def creeaza_abstract(fisier_citire, fisiere_scriere):
    r = open(fisier_citire,'r')
    w = []
    for elem in fisiere_scriere:
        w.append(open(elem,'w'))
    
    k = 0
    index = 0
    
    for linie in r:
        
        index += 1
        
        linie_crt = json.loads(linie)
        articol_crt = {}
        articol_crt['id'] = linie_crt['id']
        articol_crt['title'] = linie_crt['title']
        articol_crt['authors'] = linie_crt['authors']
        articol_crt['fos'] = linie_crt['fos']
        articol_crt['venue'] = linie_crt['venue']
        articol_crt['indexed_abstract'] = linie_crt['indexed_abstract']
        
        abstr_crt = linie_crt['indexed_abstract']
        crt_abstr_list = ""
        for elem in abstr_crt:
            for i in range(0,abstr_crt[elem]):
                crt_abstr_list += (elem + ' ')
                
        articol_crt['abstract'] = crt_abstr_list[0:len(crt_abstr_list)-1]
        w[k].write(json.dumps(articol_crt))  
        if index % 10000 == 0:
            k += 1
        else:
            w[k].write('\n')
            
    r.close()
    for i in range(0,11):
        w[i].close()
    