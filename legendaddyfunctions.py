def is_blank_line(line):
    if not line:
       return True
    
    if line[0] == ' ':
        return True

    if line[0] == '</div>':
        return True

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1
