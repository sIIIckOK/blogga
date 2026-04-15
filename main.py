#!/usr/bin/env python3

import os
from   pathlib import Path
import shutil

ROOT_PATH    = Path('./blogs/')
OUT_PATH     = Path('./output/')
OUT_IMG_PATH = OUT_PATH / 'img'

COUNT = 0
def iota(): 
    global COUNT
    COUNT+=1 


STYLE_CSS_PATH = './style.css'
STYLE_CSS      = ''
with open(STYLE_CSS_PATH, 'r') as file: 
    STYLE_CSS = file.read()
    
with open(OUT_PATH / 'style.css', 'w') as file: 
    file.write(STYLE_CSS)    
    print('Generated:', './style.css')



HTML_START_PATH = './start.txt'
HTML_MID_PATH   = './mid.txt'
HTML_END_PATH   = './end.txt'

HTML_START = ''
HTML_MID   = ''
HTML_END   = ''

with open(HTML_START_PATH, 'r') as file: HTML_START = file.read()
with open(HTML_MID_PATH,   'r') as file: HTML_MID   = file.read()
with open(HTML_END_PATH,   'r') as file: HTML_END   = file.read()

def parse_file_to_html(path):
    retstr = ''
    title = ''
    in_code_block = False
    with open(path, 'r') as file:
        lines = file.readlines()
        if len(lines) == 0: return '', ''
        title = lines[0].strip()
        lines = lines[1:]
        for l in lines:

            if l.strip().startswith('@code'):
                if not in_code_block:
                    retstr += "<pre><code>\n"
                else:
                    retstr += "</code></pre>\n"
                in_code_block = not in_code_block
                continue

            if in_code_block:
                l = l.replace("<", "&lt;").replace(">", "&gt;")
                retstr += l
                continue

            l = l.strip()
            if len(l) == 0: 
                retstr += '<br>\n'
                continue

            if l.startswith('@a'):
                l = l.removeprefix('@a').strip()
                if l == '': continue
                parts = l.rsplit(' ', 1)
                if len(parts) >= 2:
                    link_name, link_path = parts[0], parts[1] 
                    retstr += f'<a href="{link_path}">{link_name}</a>\n'
                else:
                    retstr += f'<a href="{l}">{l}</a>\n'
                continue


            if l.startswith('@img'):
                l = l.removeprefix('@img').strip()
                base_dir = Path(path).resolve().parent
                src_path = (base_dir / l).resolve()
                if l == "": continue
                l = os.path.basename(os.path.normpath(l))
                img_path = Path(l)
                img_name = img_path.stem
                ext_name = img_path.suffix

                count = 0
                temp = img_name
                while(OUT_IMG_PATH / f"{temp}{ext_name}").exists():
                    temp = img_name
                    temp+=str(count)
                    count+=1
                img_name = temp

                img_full_name = f'{img_name}{ext_name}'
                retstr += f'<img src="img/{img_full_name}"></img>'
                shutil.copy(src_path, OUT_IMG_PATH / img_full_name)
                continue

            if l.startswith('@nl'):
                retstr += '<br>\n'
                continue

            if l.startswith('@sub'):
                l = l.removeprefix('@sub').strip()
                retstr += f'<br><sub>{l}</sub>\n'
                continue

            if l.startswith('##'):
                l = l.split('##')[1].strip()
                retstr += f'<h2>{l}</h2>\n'
                continue
            if l.startswith('#'):
                l = l.split('#')[1].strip()
                retstr += f'<h1>{l}</h1>\n'
                continue
            retstr += f'<p>{l}</p>\n'
    if in_code_block: retstr += "</code></pre>\n"
    return retstr, title


def generate_page(path, title, body):
    x = HTML_START + title.capitalize() + HTML_MID + body + HTML_END
    with open(path, 'w') as file: 
        file.write(x)
    print('Generated:', path)

class ListPoint:
    title = ''
    filename = ''
    def __init__(self, title, filename):
        self.title    = title
        self.filename = filename


list_points = []

def generate_index(path, es):
    file_name = 'index.html'
    title     = 'Blogs - sIIIckok'
    body = '<ol class=\"main-list\">\n'
    for lp in list_points:
        body += f'    <li><a href="{lp.filename}.html">{lp.title}</a></li>\n'
    body += "</ol>\n"
    x = HTML_START + title + HTML_MID + body + HTML_END
    path =  os.path.join(path, file_name)
    with open(path, 'w') as file: 
        file.write(x)
    print('Generated:', path)

def has_ext(name, ext):
    s = name.split('.')
    if len(s) > 1 and name.split('.')[1] == ext: 
        return True
    return False

def main():
    os.makedirs(OUT_PATH, exist_ok = True)
    os.makedirs(OUT_IMG_PATH, exist_ok = True)
    directory = Path(ROOT_PATH)
    files = sorted(directory.glob('*'), key=lambda f: f.stat().st_mtime, reverse=True)

    for f in files:
        if f.is_file() and has_ext(f.name, 'page'):
            filename = f.name.split('.')[0]
            body, title = parse_file_to_html(str(f))
            if title == "": title = filename
            list_points.append(ListPoint(title, filename))
            output_file = OUT_PATH / f'{filename}.html'
            generate_page(output_file, title, body)

    generate_index(OUT_PATH, os.scandir(ROOT_PATH))
main()


