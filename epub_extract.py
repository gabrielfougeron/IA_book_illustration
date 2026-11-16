import os
import ebooklib
import ebooklib.epub
import html2text
import utils

root_dir = os.path.dirname(os.path.abspath(__file__))

epub_file = os.path.join(root_dir,'toto.epub')
filename_out = os.path.join(root_dir,'toto.txt')

Attempt_Latex_Sanitize = True
# Attempt_Latex_Sanitize = False

Attempt_HTML_2_Latex = True
# Attempt_HTML_2_Latex = False


book = ebooklib.epub.read_epub(epub_file)
text = ''
for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        text += item.get_content().decode()
        
html_txt = html2text.html2text(text)

if Attempt_Latex_Sanitize:
    for key, val in utils.latex_sanitize_replace.items():
        html_txt = html_txt.replace(key,val)


if Attempt_HTML_2_Latex:
    for html_tok, latex_tok in utils.html_2_latex.items():
        
        n_replaced = 0
        val_rot = (latex_tok, "}")
        n_val_rot = len(val_rot)
        
        idx_old = 0
        idx_new = html_txt.find(html_tok)
        
        while idx_new > 0:
            
            val = val_rot[n_replaced % n_val_rot]

            html_txt = html_txt.replace(html_tok, val, 1)
            
            idx_new = html_txt.find(html_tok)
            n_replaced += 1

        
with open(filename_out, 'w', encoding='utf_8') as txt_file:
    txt_file.write(html_txt)

