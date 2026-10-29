import os
import shutil


def copy_files_recursive(source_dir_path, dest_dir_path):
    if os.path.exists(dest_dir_path) == False:
        os.mkdir(dest_dir_path)
    contents = os.listdir(source_dir_path)
    for content in contents:
        source_path = os.path.join(source_dir_path, content)
        dest_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            copy_files_recursive(source_path, dest_path)