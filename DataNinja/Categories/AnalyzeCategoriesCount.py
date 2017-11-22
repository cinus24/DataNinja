import pandas as pd
import DataNinja.ConfigGenerated as cg

file_path = cg.CATEGORIES_COUNT
column_name = ["index_per_day","category", "count", "parent_id", "name", "Date"]

def read_file():
    queries = pd.read_csv(file_path,delimiter=',', engine="python", names = column_name)
    return queries

queries = read_file();