import pandas as pd
import DataNinja.DataReader.Config as Config

data_dir = Config.CATEGORIES_PATH

col_names = ["id", "parent_id", "name"]


def get_categories():
    return pd.read_csv(Config.CATEGORIES_PATH, delimiter=',', names=col_names, header=0)


def get_category(id, categories):
    row = categories[categories["id"] == id]
    return row


def get_category_name(id, categories):
    row = get_category(id, categories)
    return row.name.iloc[0]


def get_category_parent(id, categories):
    row = get_category(id, categories)
    return categories[categories["id"] == row.parent_id.iloc[0]]


def get_category_parent_name(id, categories):
    row = get_category(id, categories)
    parent = categories[categories["id"] == row.parent_id.iloc[0]]
    return parent.name.iloc[0]
