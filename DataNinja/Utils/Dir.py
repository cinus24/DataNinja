import os

from os.path import isfile, join


def list_dirs(data_dir):
    """
Lists all subdirectories in selected directory
    :param data_dir: main directory
    :return: subdirectories array
    """
    dirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    return dirs

def list_files(data_dir):
    onlyfiles = [f for f in os.listdir(data_dir) if isfile(join(data_dir, f))]
    return onlyfiles