#!/usr/bin/env python3

import os
from   pathlib import Path
import shutil

ROOT_PATH    = './blogs/'
OUT_PATH     = './output/'
OUT_IMG_PATH = './output/img/'

COUNT = 0
def iota(): 
    COUNT+=1 


STYLE_CSS_PATH = "./style.css"
STYLE_CSS      = ""
with open(STYLE_CSS_PATH, 'r') as file: 
    STYLE_CSS = file.read()
    
with open(OUT_PATH+"./style.css", 'w') as file: 
    file.write(STYLE_CSS)    
    print("Generated:", "./style.css");



HTML_START_PATH = "./start.txt"
HTML_MID_PATH   = "./mid.txt"
HTML_END_PATH   = "./end.txt"

HTML_START = ""
HTML_MID   = ""
HTML_END   = ""

with open(HTML_START_PATH, 'r') as file: HTML_START = file.read()
with open(HTML_MID_PATH,   'r') as file: HTML_MID   = file.read()
with open(HTML_END_PATH,   'r') as file: HTML_END   = file.read()

def parse_file_to_html(path):
    retstr = ""
    title = ""
    with open(path, 'r') as file:
        lines = file.readlines()
        if len(lines) == 0: return "", ""
        title = lines[0].strip()
        lines = lines[1:]
        for l in lines:
            l = l.strip()
            if len(l) == 0: 
                retstr += "<br>\n"
                continue

            if l.startswith("@img"):
                l = l.removeprefix("@img"); l.strip()
                l = l.strip()
                base_dir = Path(path).resolve().parent
                src_path = (base_dir / l).resolve()
                if l == "": continue
                l = os.path.basename(os.path.normpath(l))
                img_name = l.split('.')[0]
                ext_name = l.split('.')[1]
                count = 0
                while os.path.exists(OUT_IMG_PATH+img_name+"."+ext_name):
                    img_name+=count
                img_full_name = img_name+"."+ext_name
                retstr += "<img src="+img_full_name+"></img>"
                shutil.copy(src_path, OUT_PATH+img_full_name)
                continue

            if l.startswith("@nl"):
                retstr += "<br>\n"
                continue

            if l.startswith("@sub"):
                l = l.removeprefix("@sub"); l.strip()
                l = l.strip()
                retstr += "<br><sub>"+l+"</sub>\n"
                continue

            if l.startswith("##"):
                l = l.split('##')[1].strip()
                retstr += "<h2>"+l+"</h2>\n"
                continue
            if l.startswith("#"):
                l = l.split('#')[1].strip()
                retstr += "<h1>"+l+"</h1>\n"
                continue
            retstr += "<p>"+l+"</p>\n"
    return retstr, title


def generate_page(path, title, body):
    x = HTML_START + title.capitalize() + HTML_MID + body + HTML_END
    with open(path, "w") as file: 
        file.write(x)
    print("Generated:", path)

class ListPoint:
    title = ""
    filename = ""
    def __init__(self, title, filename):
        self.title    = title
        self.filename = filename


list_points = []

def generate_index(path, es):
    title = "index"
    body = "<ul class=\"main-list\">\n"
    for lp in list_points:
        body += "    <li><a href="+lp.filename+".html>"+lp.title+"</a></li>\n"
    body += "</ul>\n"
    x = HTML_START + title + HTML_MID + body + HTML_END
    path =  os.path.join(path, title + ".html")
    with open(path, "w") as file: 
        file.write(x)
    print("Generated:", path)

def has_ext(name, ext):
    s = name.split('.')
    if len(s) > 1 and name.split('.')[1] == ext: 
        return True
    return False

def main():
    os.makedirs(OUT_PATH, exist_ok = True)
    os.makedirs(OUT_IMG_PATH, exist_ok = True)

    for e in os.scandir(ROOT_PATH):
        if e.is_file() and has_ext(e.name, "page"):
            filename = e.name.split('.')[0]
            body, title = parse_file_to_html(e.path)
            if title == "": title = filename
            list_points.append(ListPoint(title, filename))
            generate_page(OUT_PATH+filename+".html", title, body)

    generate_index(OUT_PATH, os.scandir(ROOT_PATH))
main()


