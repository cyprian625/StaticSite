from enum import Enum 
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    counter = 0
    for char in block:
        if char == "#":
            counter += 1
        if char != "#":
            break
    if counter in range(1,7) and counter < len(block) and block[counter] == " ":
        return BlockType.HEADING
    
    if block.startswith("```\n") and block[-3:] == "```":
        return BlockType.CODE
    
    split_blocks = block.split("\n") 
    for line in split_blocks:
        if not line.startswith(">"):
            break
    else:
        return BlockType.QUOTE

    for line in split_blocks:
        if not line.startswith("- "):
            break
    else:
        return BlockType.UNORDERED_LIST
        
    expected_number = 1
    for line in split_blocks:
        prefix = f"{expected_number}. "
        if not line.startswith(prefix):
            break
        expected_number += 1
    else:
        return BlockType.ORDERED_LIST    
    return BlockType.PARAGRAPH
    
def markdown_to_blocks(markdown):
    blocks = []
    raw_blocks = markdown.split("\n\n")
    for block in raw_blocks:
        block = block.strip()
        if block != "":
            blocks.append(block)
    return blocks

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            split_block = block.split("\n")
            joined_block = " ".join(split_block)
            children_nodes = text_to_children(joined_block)
            parent_node = ParentNode("p", children_nodes)
            children.append(parent_node)

        elif block_type == BlockType.HEADING:
            counter = ""
            for char in block:
                if char == "#":
                    counter += "#"
                else:
                    break
            split_block = block.split(f"{counter} ")
            children_nodes = text_to_children(split_block[1])
            parent_node = ParentNode(f"h{len(counter)}", children_nodes)
            children.append(parent_node)

        elif block_type == BlockType.CODE:
            code = block[4:-3]
            text_node = TextNode(code, TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            parent_node = ParentNode("pre", [html_node])
            children.append(parent_node)

        elif block_type == BlockType.QUOTE:
            split_block = block.split("\n")
            cleaned = []
            for line in split_block:
                stripped_line = line.strip("> ")
                cleaned.append(stripped_line)
            joined_lines = " ".join(cleaned)
            children_nodes = text_to_children(joined_lines)
            parent_node = ParentNode("blockquote", children_nodes)
            children.append(parent_node)
                
        elif block_type == BlockType.UNORDERED_LIST:
            split_block = block.split("\n")
            cleaned = []
            for line in split_block:
                stripped_line = line.lstrip("- ")
                cleaned.append(stripped_line)
            parent_nodes = []
            for clean_line in cleaned:
                child_node = text_to_children(clean_line)
                inner_parent_node = ParentNode("li", child_node)
                parent_nodes.append(inner_parent_node)
            outer_parent_node = ParentNode("ul", parent_nodes)
            children.append(outer_parent_node)

        elif block_type == BlockType.ORDERED_LIST:
            split_block = block.split("\n")
            cleaned = []
            for i, line in enumerate(split_block, start = 1):
                prefix = f"{i}. "
                stripped_line = line.lstrip(prefix)
                cleaned.append(stripped_line)
            parent_nodes = []
            for clean_line in cleaned:
                child_node = text_to_children(clean_line)
                inner_parent_node = ParentNode("li", child_node)
                parent_nodes.append(inner_parent_node)
            outer_parent_node = ParentNode("ol", parent_nodes)
            children.append(outer_parent_node)
    html_node = ParentNode("div", children)
    return html_node

def extract_title(markdown):
        blocks = markdown_to_blocks(markdown)
        for line in blocks:
            if line.startswith("# "):
                stripped_line = line.removeprefix("# ")
                stripped_line = stripped_line.strip()
                return stripped_line
        raise Exception("no title found")