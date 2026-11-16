import os
import json
import utils

root_dir = os.path.dirname(os.path.abspath(__file__))

root_main_dir = os.path.join(root_dir, r'latex\main\A5-full')
base_dir = os.path.join(root_dir, r'latex\shared\chapters')

n_chap_max = 10

for i_chap in range(1,n_chap_max+1):
    
    chap_dirname = os.path.join(base_dir, "chapter-"+str(i_chap).zfill(2))
    os.makedirs(chap_dirname, exist_ok=True)
    
    chap_filename = os.path.join(chap_dirname, "chapter-"+str(i_chap).zfill(2)+".tex")
    
    if not os.path.exists(chap_filename):
        with open(chap_filename, 'w') as f:
            # f.write(r'\chapter{}'+"\n\n\n"+r"\image")
            f.write(r'\chapter{}'+"\n\n")