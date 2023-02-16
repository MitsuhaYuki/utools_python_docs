import json

from bs4 import BeautifulSoup
from rich.console import Console
import os

console = Console(width=150)

config = {
    'plugin_ver': '1.0.0',
    'author_name': 'MitsuhaYuki',
    'author_url': 'https://github.com/MitsuhaYuki/utools_python_docs',
    'doc_ver': '3.11.2',
    'doc_path': 'python-3.11.2-docs-html'
}

storage = {
    'indexes': [],
    'doc_path': '',
    'public_path': '',
}


def wrap_html(html_content: str):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
  <link rel="stylesheet" type="text/css" href="../_static/pygments.css" />
  <link rel="stylesheet" type="text/css" href="../_static/pydoctheme.css?2022.1" />
</head>
<body>
  {html_content}
</body>
</html>'''


def parse_reference_index():
    reference_path = f"{storage['doc_path']}\\reference"
    public_reference_path = f"{storage['public_path']}\\reference"
    toc_list = []
    if not os.path.exists(public_reference_path):
        console.log('public reference path is not exist, creating folder')
        os.mkdir(public_reference_path)
    with open(f"{reference_path}\\index.html", encoding='utf8') as f:
        raw_html = f.readlines()
        raw_html = ''.join(raw_html)
    soup = BeautifulSoup(raw_html, features="html.parser")
    level1_toc = soup.find_all('li', class_='toctree-l1')
    for level1_toc_item in level1_toc:
        chapter_dom = level1_toc_item.contents[0]
        chapter_name = chapter_dom.getText().split('. ')[1]
        chapter_link = chapter_dom['href']

        # 读取第一级
        with open(f"{reference_path}\\{chapter_link}", encoding='utf8') as f:
            raw_chapter_html = f.readlines()
            raw_chapter_html = ''.join(raw_chapter_html)
        chapter_soup = BeautifulSoup(raw_chapter_html, features="html.parser")
        chapter_content = chapter_soup.find('div', class_='body', attrs={"role": "main"})
        chapter_html = wrap_html(str(chapter_content))
        with open(f"{public_reference_path}\\{chapter_link}", 'w', encoding='utf8') as f:
            f.write(chapter_html)

        # toc_list.append({
        #     't': chapter_name,
        #     'p': f"reference/{chapter_link}",
        #     'd': f"语言参考/{chapter_name}"
        # })

        level2_toc = level1_toc_item.find_all('li', class_='toctree-l2')
        for level2_toc_item in level2_toc:
            unit_dom = level2_toc_item.contents[0]
            unit_name = unit_dom.getText().split('. ')[1]
            unit_link = unit_dom['href']

            if unit_link.find(chapter_link) == -1:
                target_file_link = unit_link
                if unit_link.find('#') != -1:
                    target_file_link = unit_link.split('#')[0]
                # 读取第一级
                with open(f"{reference_path}\\{target_file_link}", encoding='utf8') as f:
                    raw_unit_html = f.readlines()
                    raw_unit_html = ''.join(raw_unit_html)
                unit_soup = BeautifulSoup(raw_unit_html, features="html.parser")
                unit_content = unit_soup.find('div', class_='body', attrs={"role": "main"})
                unit_html = wrap_html(str(unit_content))
                with open(f"{public_reference_path}\\{target_file_link}", 'w', encoding='utf8') as f:
                    f.write(unit_html)

            toc_list.append({
                't': unit_name,
                'p': f"reference/{unit_link}",
                'd': f"语言参考/{chapter_name}/{unit_name}"
            })
    return toc_list


def parse_library_index():
    library_path = f"{storage['doc_path']}\\library"
    public_library_path = f"{storage['public_path']}\\library"
    toc_list = []
    if not os.path.exists(public_library_path):
        console.log('public library path is not exist, creating folder')
        os.mkdir(public_library_path)
    with open(f"{library_path}\\index.html", encoding='utf8') as f:
        raw_html = f.readlines()
        raw_html = ''.join(raw_html)
    soup = BeautifulSoup(raw_html, features="html.parser")
    level1_toc = soup.find_all('li', class_='toctree-l1')
    for level1_toc_item in level1_toc:
        chapter_dom = level1_toc_item.contents[0]
        chapter_name = chapter_dom.getText()
        chapter_link = chapter_dom['href']

        # 读取第一级
        with open(f"{library_path}\\{chapter_link}", encoding='utf8') as f:
            raw_chapter_html = f.readlines()
            raw_chapter_html = ''.join(raw_chapter_html)
        chapter_soup = BeautifulSoup(raw_chapter_html, features="html.parser")
        chapter_content = chapter_soup.find('div', class_='body', attrs={"role": "main"})
        chapter_html = wrap_html(str(chapter_content))
        with open(f"{public_library_path}\\{chapter_link}", 'w', encoding='utf8') as f:
            f.write(chapter_html)

        toc_list.append({
            't': chapter_name,
            'p': f"library/{chapter_link}",
            'd': f"标准库参考/{chapter_name}"
        })

        level2_toc = level1_toc_item.find_all('li', class_='toctree-l2')
        for level2_toc_item in level2_toc:
            unit_dom = level2_toc_item.contents[0]
            unit_name = unit_dom.getText()
            unit_name_cpx = unit_name
            unit_link = unit_dom['href']

            if unit_link.find(chapter_link) == -1:
                target_file_link = unit_link
                if unit_link.find('#') != -1:
                    target_file_link = unit_link.split('#')[0]
                # 读取第一级
                with open(f"{library_path}\\{target_file_link}", encoding='utf8') as f:
                    raw_unit_html = f.readlines()
                    raw_unit_html = ''.join(raw_unit_html)
                unit_soup = BeautifulSoup(raw_unit_html, features="html.parser")
                unit_content = unit_soup.find('div', class_='body', attrs={"role": "main"})
                unit_html = wrap_html(str(unit_content))
                with open(f"{public_library_path}\\{target_file_link}", 'w', encoding='utf8') as f:
                    f.write(unit_html)

            if unit_name.find(' --- ') != -1:
                split_name = unit_name.split(' --- ')
                unit_name = split_name[0]
                # unit_name_cpx = '/'.join(split_name)
                unit_name_cpx = split_name[1]

            toc_list.append({
                't': unit_name,
                'p': f"library/{unit_link}",
                'd': f"标准库参考/{chapter_name}/{unit_name_cpx}"
            })
    return toc_list


def create_plugin_meta():
    plugin_meta = {
        'version': config['plugin_ver'],
        'pluginName': f"Python {config['doc_ver']} 文档",
        'description': f"Python {config['doc_ver']} 文档速查",
        'author': config['author_name'],
        'homepage': config['author_url'],
        'preload': 'preload.js',
        'logo': 'logo.png',
        'features': [{
            'code': 'python',
            'explain': f"Python {config['doc_ver']} 文档速查",
            'cmds': [f"Python {config['doc_ver']}"]
        }]
    }
    with open(f"{storage['public_path']}\\plugin.json", 'w', encoding='utf-8') as f:
        json.dump(plugin_meta, f)
    console.log()


def start():
    console.log('start program')
    cwd = os.getcwd()
    storage['doc_path'] = f"{cwd}\\{config['doc_path']}"
    storage['public_path'] = f"{cwd}\\public"
    console.log('current cwd', storage['doc_path'])
    main_toc = []
    reference_toc = parse_reference_index()
    library_toc = parse_library_index()
    main_toc = main_toc + reference_toc + library_toc
    with open(f"{storage['public_path']}\\indexes.json", 'w', encoding='utf-8') as f:
        json.dump(main_toc, f)
    create_plugin_meta()
    console.log('convert document complete')


if __name__ == '__main__':
    start()
