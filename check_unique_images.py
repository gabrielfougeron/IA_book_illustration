import os
import utils

# error_on_first_problem = True
error_on_first_problem = False

def send_msg(msg):
    if error_on_first_problem:
        raise ValueError(msg)
    else:
        print(msg)
    
n_non_found = 0

root_dir = os.path.dirname(os.path.abspath(__file__))
project_name = os.path.split(root_dir)[-1]

root_main_dir = os.path.join(root_dir, r'latex\main\A5-full')
base_dir = os.path.join(root_dir, r'latex\shared\chapters')

match_ext_tex = ['.tex']

imgs_set = set()

for root, dirs, files in os.walk(base_dir, topdown=False):

    relroot = os.path.relpath(root, base_dir)
    
    for the_file in files:

        full_filename = os.path.join(root, the_file)
        base, ext = os.path.splitext(the_file)
        
        ignore_file = ext.lower() not in match_ext_tex
                
        if ignore_file:
            continue
        
        with open(full_filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        img_idx = [0]
        
        for i, l in enumerate(lines):
            if r"\image" in l:

                relpath = utils.find_matching_del(l, r"\image", "[", "]")[1:-1]
                fullpath = os.path.join(root_main_dir, relpath)
                
                if not os.path.exists(fullpath):
                    msg = f"File not foud : {fullpath}"
                    send_msg(msg)
                    n_non_found += 1
                
                if fullpath in imgs_set:
                    msg = f"File included twice : {fullpath}"
                    send_msg(msg)
                        
                imgs_set.add(fullpath)
                
print(f"Total number of files not found: {n_non_found}")