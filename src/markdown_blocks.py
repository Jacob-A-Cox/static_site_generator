from htmlnode import *
from inline_markdown import *
from textnode import *

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    md_to_block = markdown.split("\n\n")
    for i in md_to_block:
        if i == "":
            continue
        blocks.append(i.strip())
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_ordered_list:
        return olist_to_html_node(block)
    if block_type == block_type_unordered_list:
        return ulist_to_html_node(block)
    raise ValueError("Invalid block type")

def block_to_block_type(markdown):
    if (
        markdown.startswith("# ")
        or markdown.startswith("## ")
        or markdown.startswith("### ")
        or markdown.startswith("#### ")
        or markdown.startswith("##### ")
        or markdown.startswith("###### ")
    ):
        return block_type_heading
    
    if markdown.startswith("```") and markdown.endswith("```"):
        return block_type_code
    
    yes_quote = True
    for i in markdown.split("\n"):
        if i == "":
            continue
        if not i.startswith(">"):
            yes_quote = False
    if yes_quote:
        return block_type_quote
    
    yes_uo_list = True
    for i in markdown.split("\n"):
        if i == "":
            continue
        if not i.startswith("* ") and not i.startswith("- "):
            yes_uo_list = False
    if yes_uo_list:
        return block_type_unordered_list
    
    yes_o_list = True
    j = 1
    for i in markdown.split("\n"):
        if i == "":
            continue
        if not i.startswith(f"{j}. "):
            yes_o_list = False
        j += 1
    if yes_o_list:
        return block_type_ordered_list
    
    else:
        return block_type_paragraph

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for i in block:
        if i == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code =  ParentNode("code", children)
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("quoteblock", children)