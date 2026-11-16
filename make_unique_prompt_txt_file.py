import os
import json
import copy
import utils
import itertools

root_dir = os.path.dirname(os.path.abspath(__file__))
project_name = os.path.split(root_dir)[-1]

root_main_dir = os.path.join(root_dir, r'latex\main\A5-full')
base_dir = os.path.join(root_dir, r'latex\shared\chapters')

in_dir = os.path.join(root_dir, "output")

main_comfy_out_dir = r"E:\ComfyUI\ComfyUI\output"
out_gen_dir = os.path.join(main_comfy_out_dir, project_name)
os.makedirs(out_gen_dir, exist_ok = True)

main_comfy_in_dir = r"E:\ComfyUI\ComfyUI\input\Bookprompt"
os.makedirs(main_comfy_in_dir, exist_ok = True)

json_filename = os.path.join(in_dir, "imgs.json")

t2s_prompts_filename = os.path.join(main_comfy_in_dir, "t2s_prompts.txt")
t2s_paths_filename = os.path.join(main_comfy_in_dir, "t2s_paths.txt")

img_prompts_filename = os.path.join(main_comfy_in_dir, "img_prompts.txt")
img_paths_filename = os.path.join(main_comfy_in_dir, "img_paths.txt")
img_loras_filename = os.path.join(main_comfy_in_dir, "img_loras.txt")

all_t2s_prompts = ""
all_t2s_paths = ""

all_img_prompts = ""
all_img_loras = ""
all_img_paths = ""

replace_dict = {
    "\n" : ""   ,
}

remove_trigger = True
# remove_trigger = False

prompt_start_str = ""

trigger_Loras_dict_stack = {
    "<Harry>" : r"<lora:Krea 2\Enfants\Tristan.safetensors:1.5:1.5>",
    "<Hermione>" : r"<lora:Krea 2\Enfants\Raphaelle.safetensors:1.5:1.5>",
    "<Ron>" : r"<lora:Krea 2\Enfants\Marin.safetensors:1.5:1.5>",
    "<harry>" : r"<lora:Krea 2\Enfants\Tristan.safetensors:1.5:1.5>",
    "<hermione>" : r"<lora:Krea 2\Enfants\Raphaelle.safetensors:1.5:1.5>",
    "<ron>" : r"<lora:Krea 2\Enfants\Marin.safetensors:1.5:1.5>",
    "<HARRY>" : r"<lora:Krea 2\Enfants\Tristan.safetensors:1.5:1.5>",
    "<HERMIONE>" : r"<lora:Krea 2\Enfants\Raphaelle.safetensors:1.5:1.5>",
    "<RON>" : r"<lora:Krea 2\Enfants\Marin.safetensors:1.5:1.5>",
}

trigger_Loras_dict_nostack = {
    # "princess" : r"<lora:Krea 2\Enfants\Raphaelle.safetensors:1.5:1.5>",
    # "apprentice" : r"<lora:Krea 2\Enfants\Marin.safetensors:1.5:1.5>",
    # "boy" : r"<lora:Krea 2\Enfants\Marin.safetensors:1.5:1.5>",
    # "man" : r"<lora:Krea 2\Enfants\Tristan.safetensors:1.5:1.5>",
    # "prince" : r"<lora:Krea 2\Enfants\Tristan.safetensors:1.5:1.5>",
}

default_Lora = ""
# default_Lora = r"<lora:Krea 2\style_illustration\Nature_Krea2.safetensors:1.0:1.0>"
# 
select_only_if_img_filename_contains = []
# select_only_if_img_filename_contains = ["001.jpg"]

select_only_if_img_filename_contains = [
    "chapter-03\\009",
    "chapter-05\\006",
    "chapter-06\\004",
    "chapter-08\\002",
    "chapter-08\\003",
    "chapter-09\\003",
    "chapter-09\\006",
    "chapter-09\\009",
    "chapter-09\\010",
    "chapter-11\\003",
    "chapter-11\\004",
    "chapter-11\\007",
    "chapter-12\\004",
    "chapter-13\\002",
    "chapter-13\\011",
    "chapter-13\\013",
    "chapter-15\\011",
    "chapter-16\\005",
    "chapter-16\\006",
    "chapter-16\\007",
    "chapter-16\\008",
    "chapter-17\\009",
    "chapter-18\\001",
    "chapter-18\\005",
    "chapter-20\\007",
    "chapter-22\\009",
    "chapter-22\\010",
    "chapter-24\\002",
    "chapter-25\\007",
    "chapter-26\\001",
    "chapter-26\\013",
    "chapter-29\\006",
    "chapter-29\\010",
    "chapter-30\\004",
    "chapter-30\\008",
    "chapter-30\\012",
    "chapter-31\\004",
    "chapter-32\\002",
    "chapter-32\\003",
    "chapter-32\\006",
    "chapter-33\\001",
    "chapter-33\\002",
    "chapter-33\\006",
    "chapter-34\\002",
    "chapter-34\\003",
    "chapter-35\\001",
    "chapter-37\\004",
    "chapter-37\\007",
    "chapter-37\\008",
]


if replace_dict:
    for key in itertools.chain(trigger_Loras_dict_stack, trigger_Loras_dict_nostack):
        replace_dict[key] = ""

with open(json_filename, encoding="utf-8") as f:
    all_imgs = json.load(f)
    
n_img_prompts = 0
n_t2s_prompts = 0
    
for img_filename, img_dict in all_imgs.items():
    
    select_me = len(select_only_if_img_filename_contains) == 0
    for key in select_only_if_img_filename_contains:
        if key in img_filename:
            select_me = True
    
    if not(select_me):
        continue

    img_prompts = img_dict.get("img_prompts",[])
    
    img_dirname = os.path.normpath(img_filename[:-4])
    img_dirname_list = img_dirname.split(os.sep)
    
    path = os.path.join(out_gen_dir, img_dirname_list[-2], img_dirname_list[-1])
    
    for prompt_ini in img_prompts:
        
        prompt = copy.copy(prompt_ini)
        
        prompt = prompt_start_str + prompt
        
        lora = ""
        
        n_trigger = 0
        for key, val in trigger_Loras_dict_stack.items():
            if key in prompt:
                lora = lora + " " + val
                n_trigger += 1
                
        lora = lora + " " + default_Lora
                
        # if n_trigger == 0:
        #     lora = lora + " " + default_Lora
        
        for key, val in trigger_Loras_dict_nostack.items():
            if key in prompt:
                lora = lora + " " + val
                break
            
        for key, val in replace_dict.items():
            prompt = prompt.replace(key,val)
            
        all_img_prompts += prompt + '\n'
        all_img_loras += lora + '\n'
        all_img_paths += path + '\n'
            
        n_img_prompts += 1
        
    t2s_prompt = img_dict.get("t2s_prompt","")
    for key, val in replace_dict.items():
        t2s_prompt = t2s_prompt.replace(key,val)
    
    n_t2s_prompts += 1

    all_t2s_prompts += t2s_prompt + '\n'
    all_t2s_paths += path + '\n'
            
with open(t2s_prompts_filename, "w", encoding="utf-8") as f:
    f.write(all_t2s_prompts)
    
with open(t2s_paths_filename, "w", encoding="utf-8") as f:
    f.write(all_t2s_paths)        
    
with open(img_prompts_filename, "w", encoding="utf-8") as f:
    f.write(all_img_prompts)  
      
with open(img_loras_filename, "w", encoding="utf-8") as f:
    f.write(all_img_loras)
    
with open(img_paths_filename, "w", encoding="utf-8") as f:
    f.write(all_img_paths)
    
    
print(f"Number of image prompts: {n_img_prompts}")
print(f"Number of T2S prompts: {n_t2s_prompts}")