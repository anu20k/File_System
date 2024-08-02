import os
from functools import reduce

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir.
    """
    structure = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1

    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = {name: {} for name in dirs}
        subdir.update({name: None for name in files})
        parent = reduce(dict.get, folders[:-1], structure)
        parent[folders[-1]] = subdir

    
    return structure


