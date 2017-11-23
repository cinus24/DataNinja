import pickle

from DataNinja.DataReader.QueryReader import get_selected_queries
from DataNinja.Utils.Dir import list_dirs

"""
Saving and loading object to/from files
"""

def save_obj(obj, name ):
    """
Saves object to .pkl file (Warning! - big files may be created)
    :param obj: Object to save
    :param name: Filename
    """
    with open('saved/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    """
Loads object from .pkl file
    :param name: Filename to load
    :return: Loaded object
    """
    with open(name, 'rb') as f:
        return pickle.load(f)

def save_queries_to_files(data_dir):
    """
Saves all queries csv's from data directory to separate files
    :param data_dir:
    """
    max_days = 14
    month_strings = list_dirs(data_dir)
    for month in month_strings:
        queries_dict = get_selected_queries(max_days, month)
        save_obj(queries_dict, month)