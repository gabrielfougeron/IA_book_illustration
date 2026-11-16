import os
import json
import utils

root_dir = os.path.dirname(os.path.abspath(__file__))

root_main_dir = os.path.join(root_dir, r'latex\main\A5-full')
base_dir = os.path.join(root_dir, r'latex\shared\chapters')
out_dir = os.path.join(root_dir,"output")

match_ext_tex = [".tex"]

n_lines_since_img_threshold = 70

for root, dirs, files in os.walk(base_dir, topdown=False):
    
    for the_file in files:

        full_filename = os.path.join(root, the_file)
        base, ext = os.path.splitext(the_file)
        
        ignore_file = ext.lower() not in match_ext_tex
                
        if ignore_file:
            continue
        
        with open(full_filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        n_lines_since_img = 0
        
        for img_idx, l in enumerate(lines):
            
            if r"\image" in l:
                n_lines_since_img = 0
                continue
            
            if len(l) > 1:
                n_lines_since_img += 1
            else:

                if n_lines_since_img > n_lines_since_img_threshold:
                    n_lines_since_img = 0
                    
                    lines[img_idx] = "\n\\image\n\n"
                    
                
        with open(full_filename, "w", encoding="utf-8") as f:
            f.write("".join(lines))
            
            