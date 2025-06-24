import os
import shutil
from pathlib import Path

from textnode import TextNode, TextType
from blocks_markdown import (
    markdown_to_blocks,
    markdown_to_html_node
)

def copy_source_to_destination(source="static", destination="public"):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.makedirs(destination)
    
    def copy(source, destination):
        for item in os.listdir(source):
            source_item = os.path.join(source, item)
            destination_item = os.path.join(destination, item)

            if os.path.isdir(source_item):
                os.makedirs(destination_item, exist_ok=True)
                copy(source_item, destination_item)
            else:
                 shutil.copy2(source_item, destination_item)

    copy(source, destination)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("#"):
            return block

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as from_file:
        content = from_file.read()
    
    with open(template_path, "r") as template_file:
        template = template_file.read()

    html_nodes = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    new_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_nodes)
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir) 
        
    with open(dest_path, "w") as output_file:
        output_file.write(new_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

def main():
    copy_source_to_destination()
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
