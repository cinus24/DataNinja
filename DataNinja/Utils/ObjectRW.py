import pickle

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

def load_obj(name ):
    """
Loads object from .pkl file
    :param name: Filename to load
    :return: Loaded object
    """
    with open('saved/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)