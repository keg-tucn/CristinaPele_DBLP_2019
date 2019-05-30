import json

###
### Get field from json file.
### param field: the requested field.
### param filePath: path to the json file.
### param unique: uniquiness of the elements in the returning list (optional, default true).
### param current_list: the list with all the fields requested from file (optional, default []).
### return current_list: a list with all the fields requested form the file.
###
def get_field(field, filePath, unique = True, current_list = []):
    r = open(filePath, 'r')
    for line in r:
        crt_line = json.loads(line)
        current_list.append(crt_line[field])
    
    if unique == True:
        current_list = list(dict.fromkeys(current_list))
        
    r.close()
    return current_list

###
### Get field of fields from json file.
### param field_list: list with the requested field (position 0) and the requsted subfield of the (positon 1).
### param filePath: path to the json file.
### param unique: uniquiness of the elements in the returning list (optional, default true).
### param current_list: the list with all the fields requested from file (optional, default []).
### return current_list: a list with all the fields requested form the file.
###
def get_field_of_field(field_list, filePath, current_list = [], unique = True):
    r = open(filePath, 'r')
    for line in r:
        crt_line = json.loads(line)
        crt_line = crt_line[field_list[0]]
        for elem in crt_line:
            current_list.append(elem[field_list[1]])
    
    if unique == True:
        current_list = list(dict.fromkeys(current_list))
    r.close()
    return current_list


