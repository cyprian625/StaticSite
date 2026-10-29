from markdown_blocks import extract_title, markdown_to_html_node
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_path_md = f.read()
    with open(template_path) as f:
        template_md = f.read()
    from_path_nodes = markdown_to_html_node(from_path_md) 
    from_path_html = from_path_nodes.to_html()
    title = extract_title(from_path_md)
    template_md = template_md.replace("{{ Title }}", title)
    template_md = template_md.replace("{{ Content }}", from_path_html)
    dest_path_directory = os.path.dirname(dest_path)
    if os.path.dirname(dest_path) != "":
        os.makedirs(dest_path_directory, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_md)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for content in contents:
        source_path = os.path.join(dir_path_content, content)
        if os.path.isfile(source_path):
            content_html = content.replace(".md", ".html")
            dest_dir_html = os.path.join(dest_dir_path, content_html)
            generate_page(source_path, template_path, dest_dir_html)
        else:
            new_dest_dir_path = os.path.join(dest_dir_path, content)
            generate_pages_recursive(source_path, template_path, new_dest_dir_path)
                



