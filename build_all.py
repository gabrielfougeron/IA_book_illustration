import sys
import os
import shutil
import subprocess
import concurrent.futures
import multiprocessing
import argparse
import datetime
import locale
import imagesize
import functools
from PIL import Image, ImageFilter
import numpy as np

root_dir = os.path.dirname(os.path.abspath(__file__))
project_name = os.path.split(root_dir)[-1]

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

parser = argparse.ArgumentParser(
    description = 'Builds all latex files and copies pdf in output folder',
)

parser.add_argument(
    '-v', '--verbose'                   ,        
    action = 'store_true'               ,
    dest = 'verbose'                    ,
    help = f'Sets output to verbose'    ,
)

parser.add_argument(
    '-C', '--clean'                 ,        
    action = 'store_true'           ,
    dest = 'clean_latex'            ,
    help = f'Cleans before build'   ,
)

parser.add_argument(
    '-f', '--force'                 ,        
    action = 'store_true'           ,
    dest = 'force_latex'            ,
    help = f'Force build'           ,
)

parser.add_argument(
    '-n'                                        ,    
    action = 'store'                            ,
    dest = 'n_threads'                          ,
    type = int                                  ,
    default = multiprocessing.cpu_count()       ,
    help = f'Number of parallel build threads'  ,
)

parser.add_argument(
    '-doc'                                      ,    
    action = 'store'                            ,
    dest = 'build_doc'                          ,
    type = str                                  ,
    default = "all"                             ,
    help = '''Latex document to be built.\n
all: builds all documents\n
none: builds no documents\n
doc_name: builds only document doc_name\n
''',
)

args = parser.parse_args(sys.argv[1:])

subprocess_kwargs = {
    "stdout" : subprocess.PIPE      ,
    "stderr" : subprocess.PIPE      ,
}

base_dir = os.path.dirname(__file__)
out_dir = os.path.join(base_dir, "output")

if not os.path.isdir(out_dir):
    os.makedirs(out_dir)
    
latex_main_dir = os.path.join(base_dir, "latex", "main")
latex_shared_dir = os.path.join(base_dir, "latex", "shared")
autogen_shared_dir = os.path.join(base_dir, "latex", "auto_generated")

def make_pdf(name):
    
    fullname = os.path.join(latex_main_dir, name)
    
    if not os.path.isdir(fullname):
        raise ValueError(f"Unknown document : {name}")
    
    print(f"Building {name}")
    
    if args.clean_latex:
        cmdlist = ["latexmk", "-C"]
        p = subprocess.Popen(cmdlist, cwd=fullname, **subprocess_kwargs)
        p.wait()
    
    cmdlist = ["latexmk"]
    if args.clean_latex:
        cmdlist.append("-f")
    
    p = subprocess.Popen(cmdlist, cwd=fullname, **subprocess_kwargs)
    
    out_list = []
    if args.verbose:        
        for std_item in (p.stdout, p.stderr):
            for l in iter(std_item.readline, b''):
                    
                d = l.decode("utf-8", errors="ignore")
                out_list.append(d)
                d = d.strip(os.linesep)
                d = d.strip('\n')
                if d != '':
                    print(d)

        out_data = "".join(out_list)

    else:
        
        output, errors = p.communicate()
        p.wait()
        out_data = output.decode("utf-8", errors="ignore") + os.linesep + errors.decode("utf-8", errors="ignore")

    message = out_data.lower()
    
    n_char_before = 300
    n_char_after = 100
    
    i_err = message.find("error")

    if i_err > 0:
        
        i_beg = max(i_err - n_char_before, 0)
        i_end = min(i_err + n_char_after, len(message))
        sub_message = message[i_beg:i_end]
        
        raise ValueError(f"Build failed in file {name}: {os.linesep}{os.linesep}{sub_message}")

    name_add = ""

    built_pdf_file = os.path.join(latex_main_dir, name, "build", "main.pdf")
    store_pdf_file = os.path.join(out_dir, project_name + "_"+name+name_add+".pdf")

    if os.path.isfile(built_pdf_file):

        if os.path.isfile(store_pdf_file):
            os.remove(store_pdf_file)
        
        shutil.move(built_pdf_file, store_pdf_file)
        
    print(f"Done building {name}")

match_ext_img = ['.jpg', '.jpeg', '.png', '.webp']

if __name__ == "__main__":

    if args.build_doc == "all":
        name_list = os.listdir(latex_main_dir)
    elif args.build_doc == "none":
        name_list = []
    else:
        name_list = [args.build_doc]

    if args.n_threads == 1:
        
        for name in name_list:
            make_pdf(name)
        
    else:

        with concurrent.futures.ProcessPoolExecutor(max_workers = args.n_threads) as executor:
            
            res = []
            for name in name_list:
                res.append(executor.submit(make_pdf, name))
    
    print()
    print(f"Done building {args.build_doc} !")
