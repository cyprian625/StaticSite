import shutil
import os
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
import sys 
def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    if os.path.exists("docs") == True:
        shutil.rmtree("docs")
    copy_files_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
main()
