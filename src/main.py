from textnode import *
from htmlnode import *
from inline_markdown import *
from markdown_blocks import *
from generate_page import *
import os
import shutil

#def main():
#    test_node = TextNode("This is a text node", "bold", "https://www.dev.boot")
#    print(test_node)
    
def get_paths(path):
    file_paths = []
    paths = os.listdir(path)
    for res in paths:
        if os.path.isfile(f"{path}/{res}"):
            file_paths.append(f"{path}/{res}")
        else:
            if not os.path.exists(f"{path}/{res}"):
                os.mkdir(f"{path}/{res}")
            new_paths = get_paths(f"{path}/{res}")
            for new_paths in new_paths:
                file_paths.append(new_paths)
    return file_paths

def prep_paths(paths):
    new_paths = []
    new_directories = []
    for path in paths:
        new_path = path.split("/", 1)
        new_paths.extend(new_path[1:])
    for path in paths:
        count = 0
        for i in path:
            if i == "/":
                count += 1
        if count > 1:
            shave_old_dir = path.split("/", 1)
            new_directory = shave_old_dir[1].rsplit("/", 1)
            new_directories.extend(new_directory[:1])
    for i in range(len(new_paths)):
        new_paths[i] = "public/" + new_paths[i]
    for i in range(len(new_directories)):
        new_directories[i] = "public/" + new_directories[i]
    return new_paths, new_directories

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")

    src_paths = get_paths("static")
    dst_paths, dst_directories = prep_paths(src_paths)

    for i in range(len(dst_directories)):
        os.mkdir(dst_directories[i])
    for i in range(len(src_paths)):
        shutil.copy(src_paths[i], dst_paths[i])

    generate_page("content/index.md", "template.html", "public/index.html")


    
main()


