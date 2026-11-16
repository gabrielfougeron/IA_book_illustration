- Rename top level project directory to the project name
- Find Epub
- Use `epub_extract.py` to extract epub to plain text file
- Edit `title_settings.tex`
- Get number of chapters from epub, and create empty tex chapter files using `Make_empty_chapters.py`
- edit `structure.tex` to `\input` all chapter files
- Manually copy-paste chapter content in tex chapter files.
- Get the document to a Latex compilable state, using `build_all.py` Example usage: `python build_all.py -doc A5-full -n 1 -C`
- Now is a good time to backup, and/or track the project using git
- Insert `\image` locations using `Insert_imgs_latex.py`. Caution : multiple calls to the script WILL mess up the project.
- Use `List_imgs.py` to create 'imgs.json'

Then, iterate the following until satisfaction. We recommend trying styles out on a small sample of images (Now is the computation intensive bit)

- In `qwen_create_prompts.py`, write a satisfactory prompt guiding the style of the image prompts to be generated, and generate prompts. These prompts are kept in 'imgs.json'.
- Gather prompts, Loras and paths using `make_unique_prompt_txt_file.py`
- In Comfyui, generate images, and copy/paste them in the `output` directory
- 1 directory = 1 image. Only keep the best candidate, delete the others.
- Copy these images into the Latex directory using `pick_images.py`
- Build project using `build_all.py`

Whenever something goes wrong (and they will), you can:
    - List the problem prompts in `qwen_create_prompts.py` and `make_unique_prompt_txt_file.py` to only regenerate these
    - Manually edit 'imgs.json' if need be