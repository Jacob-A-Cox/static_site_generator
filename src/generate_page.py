from htmlnode import *
from markdown_blocks import *
import os

def extract_title(markdown):
    text = markdown.split("\n")
    if not text[0].startswith("#"):
        raise ValueError("Invalid markdown: needs h1 header")
    return text[0].strip("# ")
    
def get_content(from_path):
    with open(from_path) as f:
        return f.read()
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    text = get_content(from_path)
    template = get_content(template_path)
    title = extract_title(text)
    text = markdown_to_html_node(text)
#    print(text)
    text = text.to_html()
#    print(text)
#    print(template)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", text)
#    print(template)
    new_dir = os.path.dirname(dest_path)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    f = open(dest_path, "w")
    f.write(template)
    f.close()
