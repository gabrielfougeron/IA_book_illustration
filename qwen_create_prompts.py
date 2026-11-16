import requests
import os
import json
import pyquickbench
import tqdm
import copy

TT = pyquickbench.TimeTrain()

OLLAMA_URL = "http://localhost:11434/api/chat"

MODEL_NAME = "qwen3.8:27b"

n_prompts_per_img = 6

SYSTEM_PROMPT = f"""You are an expert prompt engineer for image generation. Prompts are written in English.
The provided text is an excerpt of a children's book in French.
Please write {n_prompts_per_img} very different detailled prompts to provide varied ilustrations for this excerpt.
In terms of style, you will target a dark fantasy manga illustration.
The prompt should consist in precise description of the visual elements present in the image, and should not reference specificities of the story (ex: precise name of character or artifacts).
Each prompt will be written on a single ligne (a very long one if need be). You will only output said prompts. No numerotation or comments.
"""

root_dir = os.path.dirname(os.path.abspath(__file__))

root_main_dir = os.path.join(root_dir, r'latex\main\A5-full')
base_dir = os.path.join(root_dir, r'latex\shared\chapters')
out_dir = os.path.join(root_dir, "output")

json_filename = os.path.join(out_dir, "imgs.json")

select_only_if_img_filename_contains = []
# select_only_if_img_filename_contains = ["001.jpg"]
# select_only_if_img_filename_contains = ["chapter-01"]

# select_only_if_img_filename_contains = [
#     "chapter-06\\007",
#     "chapter-06\\008",
#     "chapter-06\\009",
# ]


def run_vlm(input_txt):
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": input_txt,
                # "images": [encode_image(image_path)]
            }
        ],
        "stream": False,
        "think": True,
        # "options" : {
        #     "temperature": 0.2,
        #     "top_p": 0.9,
        # }
    }

    output = requests.post(OLLAMA_URL, json=payload)
    output.raise_for_status()

    return output.json()

def get_response(vlm_output):
    
    response = vlm_output["message"]["content"]
    thinking = vlm_output["message"].get("thinking")

    return response, thinking

match_ext_tex = [".tex"]

with open(json_filename, encoding="utf-8") as f:
    all_imgs = json.load(f)
    
all_imgs_out = copy.deepcopy(all_imgs)

for img_filename, img_dict in tqdm.tqdm(all_imgs.items(), total=len(all_imgs)):
    
    select_me = len(select_only_if_img_filename_contains) == 0
    for key in select_only_if_img_filename_contains:
        if key in img_filename:
            select_me = True
    
    if not(select_me):
        continue
    
    
    img_prompts = img_dict.get("img_prompts",[])
    
    if len(img_prompts) < n_prompts_per_img:

        with open(img_dict["path_to_tex"], "r", encoding="utf-8") as f:
            lines = f.readlines()

        # txt = ''.join(lines[img_dict["txt_line_start"]+1:img_dict["txt_line_end"]])
        
        txt = (
            "----- Here is the whole chapter for context -----\n" +
            ''.join(lines) + "\n\n"   +
            "----- Here is the specific excerpt you need to illustrate -----\n" +
            ''.join(lines[img_dict["txt_line_start"]+1:img_dict["txt_line_end"]])
        )
            
        vlm_output = run_vlm(txt)
        response, thinking = get_response(vlm_output)
        
        response_lines = response.split("\n")
        
        sanitized_response = [s for s in response_lines if len(s) > 3]

        img_prompts.extend(sanitized_response)
        
        all_imgs_out[img_filename]["img_prompts"] = img_prompts
        
        with open(json_filename, "w", encoding="utf-8") as jsonFile:
            jsonString = json.dumps(all_imgs_out, indent=4, sort_keys=False, ensure_ascii=False)
            jsonFile.write(jsonString)

        
    

