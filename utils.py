
def find_between_str(input_string, del_l, del_r=None):
    
    if del_r is None:
        del_r = del_l
        
    return find_between_str_ann(input_string, del_l, del_r, 0, len(input_string), [])

def find_between_str_ann(input_string, del_l, del_r, ibeg, iend, res_so_far=[]):
    
    try:
        i_l = input_string.index(del_l, ibeg, iend) + len(del_l)
        i_r = input_string.index(del_r, i_l, iend)
        
        res_so_far.append(input_string[i_l:i_r])
        
        return find_between_str_ann(input_string, del_l, del_r, i_r, iend, res_so_far)
    
    except ValueError:
        return res_so_far

def find_matching_del(input_string, header, del_l, del_r=None):

    if del_r is None:
        del_r = del_l

    ibeg = input_string.index(header) + len(header)

    assert input_string[ibeg:ibeg+len(del_l)]  == del_l

    try:
    
        depth = 1
        try:
            i_l = input_string.index(del_l, ibeg+len(del_l)) + len(del_l)
        except:
            i_l = len(input_string)
            
        i_r = input_string.index(del_r, ibeg)

        while True:
            if i_r <= i_l:
                depth -= 1
                if depth == 0:
                    break
                i_r = input_string.index(del_r, i_r+len(del_r))
                
            else:
                depth += 1
                try:
                    i_l = input_string.index(del_l, i_l+len(del_l))
                except:
                    i_l = len(input_string)
    
    except ValueError:
        pass
    
    if depth > 0:
        raise ValueError
    else:
        return input_string[ibeg+1:i_r]
        
html_2_latex = {
    "_" : "\\textit{",
    "**" : "\\textbf{",
}

latex_sanitize_replace = {
    '’'     : "'"           ,
    '#'     : "\\#"         ,
    ' &'    : " \\&"        ,
    '–'     : "-"           ,
    '−'     : "-"           ,
}

puctuation_spaceafter_list = [",", "."]
puctuation_bothspace_list = [":", "?", "!"]
puctuation_list = puctuation_spaceafter_list + puctuation_bothspace_list

for punct in puctuation_spaceafter_list:
    latex_sanitize_replace[punct] = punct+" "
    latex_sanitize_replace[punct+"  "] = punct+" "

for punct in puctuation_bothspace_list:
    latex_sanitize_replace[punct] = " "+punct+" "
    latex_sanitize_replace[punct+"  "] = punct+" "
    latex_sanitize_replace["  "+punct] = " "+punct
