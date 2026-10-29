import shutil
import os
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
def main():
    if os.path.exists("public") == True:
        shutil.rmtree("public")
    copy_files_recursive("static", "public")
    generate_pages_recursive("content", "template.html", "public")
main()
