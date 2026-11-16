import os
import json
import utils

root_dir = os.path.dirname(os.path.abspath(__file__))

root_main_dir = os.path.join(root_dir, r'latex\main\A5-full')
base_dir = os.path.join(root_dir, r'latex\shared\chapters')
out_dir = os.path.join(root_dir,"output")

json_filename = os.path.join(out_dir, "imgs.json")

if os.path.exists(json_filename):
    try:
        with open(json_filename, encoding="utf-8") as f:
            all_imgs_old = json.load(f)
    except:
        all_imgs_old = {}
        
else:
    all_imgs_old = {}
    
# all_imgs_old = {}
    
match_ext_tex = [".tex"]

all_imgs = {}

Force_Image_Names = False
# Force_Image_Names = True

Attempt_Latex_Sanitize = True
# Attempt_Latex_Sanitize = False

for root, dirs, files in os.walk(base_dir, topdown=False):
    
    for the_file in files:

        full_filename = os.path.join(root, the_file)
        base, ext = os.path.splitext(the_file)
        
        ignore_file = ext.lower() not in match_ext_tex
                
        if ignore_file:
            continue

        with open(full_filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        i_img = 0
        img_idx_prev = -1
        img_fullpath_list = []
        
        WriteChapter = Attempt_Latex_Sanitize
        
        for img_idx, l in enumerate(lines):
            
            if r"\image" in l:

                i_img += 1    

                if (r"\image[" in l) and (not Force_Image_Names):
                    img_relpath = utils.find_matching_del(l, r"\image", "[", "]")[1:-1]
                    img_fullpath = os.path.normpath(os.path.join(root_main_dir, img_relpath))

                else:
                    i_img_str = str(i_img).zfill(3)
                    img_fullpath = os.path.join(root, i_img_str+".jpg")
                    img_relpath = os.path.relpath(img_fullpath, start=root_main_dir)
                    
                    lines[img_idx] = r'\image["'+img_relpath.replace("\\", "/")+r'"]'+'\n'
                    WriteChapter = True
                    
                img_dict = {
                    "path_to_tex"       : full_filename ,
                    "txt_line_start"    : img_idx_prev  ,
                    "txt_line_end"      : img_idx       ,
                }
                
                assert img_fullpath not in all_imgs
                
                all_imgs[img_fullpath] = img_dict

                img_idx_prev = img_idx
                
            if Attempt_Latex_Sanitize:
                for key, val in utils.latex_sanitize_replace.items():
                    lines[img_idx] = lines[img_idx].replace(key,val)

        if WriteChapter:     
            with open(full_filename, "w", encoding="utf-8") as f:
                f.write("".join(lines))
                            
all_imgs_fuse = {}
                            
for key, val in all_imgs.items():
    
    img_dict = all_imgs_old.get(key, {})
    
    img_dict["path_to_tex"]     = val["path_to_tex"]
    img_dict["txt_line_start"]  = val["txt_line_start"]
    img_dict["txt_line_end"]    = val["txt_line_end"]
    
    all_imgs_fuse[key] = img_dict
    
print(f"Found {len(all_imgs_fuse)} images")
       
with open(json_filename, "w", encoding="utf-8") as jsonFile:
    jsonString = json.dumps(all_imgs_fuse, indent=4, sort_keys=False)
    jsonFile.write(jsonString)

