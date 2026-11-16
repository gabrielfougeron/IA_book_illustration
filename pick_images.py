import os
import shutil
import json
import random

root_dir = os.path.dirname(os.path.abspath(__file__))

root_main_dir = os.path.join(root_dir, r'latex\main\A5-full')
base_dir = os.path.join(root_dir, r'latex\shared\chapters')
out_dir = os.path.join(root_dir,"output")
base_imgs_dir = out_dir

match_ext_img = [".jpg", ".png"]

for root, dirs, files in os.walk(base_imgs_dir, topdown=False):
    
    relroot = os.path.relpath(root, start = base_imgs_dir)
    dest = os.path.join(base_dir, relroot)

    imgs_list = []

    for the_file in files:
        
        filename = os.path.join(root, the_file)
        base, ext = os.path.splitext(the_file)

        if ext.lower() in match_ext_img:
            imgs_list.append(filename)
            
    if len(imgs_list) > 1:
        print(f"Warning: {len(imgs_list)} files found for image {root}")

    if len(imgs_list) > 0:
        chosen_img = random.choice(imgs_list)
        base, ext = os.path.splitext(chosen_img)
        shutil.copy(chosen_img, dest+ext)
        
