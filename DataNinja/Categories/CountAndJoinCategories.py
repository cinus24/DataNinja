import pandas as pd
import os
import DataNinja.DataReader.Config as config

max_days = 168
data_dir = config.QUERIES_DATA_CATALOG
categories_dir = config.CATEGORIES_PATH

index_query = 0
index_category = 1
index_count = 2

daily_queries = []
col_names = ["query", "category", "count"]
categories_col_names = ["category", "parent_id", "name"]

def convert_query(a):
    if a is None:
        return ""
    return str(a.strip('"'))

def convert_category(a):
    if a is None:
        return -1
    a = a.strip('"')
    a = a.strip(',')
    a = a.strip('"')
    return a
    #return int(a)

def convert_count(a):
    if a is None:
        return 0
    a = a.strip('"')
    a = a.strip(',')
    a = a.strip('"')
    return int(a)

def count_categories(queries_category, categories, date):
    queries_category = queries_category.drop('query', 1);
    queries_category = queries_category[queries_category.category.notnull()]
    queries_category = queries_category.groupby('category', as_index=False).sum();
    queries_category = queries_category.sort_values(by=["count"], ascending=False)
    queries_category = pd.merge(queries_category, categories, how='left', on='category')
    queries_category['Date'] = date
    queries_category.reset_index(drop=True)
    with open('CategoriesCount.csv', 'a') as f:
        queries_category.to_csv(f, header=True)

def read_categories():
    categories = pd.read_csv(categories_dir, names = categories_col_names)
    categories = categories[1:]
    return categories;


converters = {index_query:convert_query, index_category:convert_category, index_count: convert_count}
categories = read_categories();
for file_index, file_name in enumerate(os.listdir(data_dir)):
        if file_index < max_days:
            print(file_index)
            if file_index != 67 and file_index != 105:
                p = os.path.join(data_dir, file_name)
                queries = pd.read_csv(p,delimiter='","', engine="python", header =0, names = col_names, quotechar='"',
                                   converters=converters)

                count_categories(queries, categories, file_name[15:len(file_name)-4]);
