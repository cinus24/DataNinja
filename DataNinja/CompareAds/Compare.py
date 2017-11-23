import DataNinja.DataReader.AdsReader as ad
import pandas as pd
import DataNinja.DataReader.CategoriesReader as cr

keys = ['2016_11_01.csv', '2016_12_01.csv', '2017_01_01.csv', '2017_02_01.csv', '2017_03_01.csv', '2017_04_01.csv', '2017_05_01.csv', '2017_06_01.csv', '2017_07_01.csv', '2017_08_01.csv', '2017_09_01.csv']

def categories():
        col_names = ["category_id", "parent_id", "name"]
        categories = cr.get_categories()
        categories.columns = col_names
        categories = categories.drop('parent_id', 1)
        return categories

def prepare_ads(key, categories):
        df= ads[key]
        df = df.drop('sold', 1)
        df = df.drop('id', 1)
        df = df.drop('region_id', 1)
        df = df.drop('replies', 1)
        df = df.drop('views', 1)
        df = df[df.category_id.notnull()]
        df = df['category_id'].value_counts().reset_index()
        df.columns = ['category_id', 'count']

        df = pd.merge(df, categories, how='left', on='category_id')
        df = df[df.name.notnull()]

categories = categories()
ads = ad.get_ads_clean(12)
for key in keys:
       prepare_ads(key, categories)

