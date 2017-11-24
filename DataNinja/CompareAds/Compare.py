import DataNinja.DataReader.AdsReader as ad
import pandas as pd
import DataNinja.DataReader.CategoriesReader as cr
import matplotlib.pyplot as plt

keys = ['2016_11_01.csv', '2016_12_01.csv', '2017_01_01.csv', '2017_02_01.csv', '2017_03_01.csv', '2017_04_01.csv', '2017_05_01.csv', '2017_06_01.csv', '2017_07_01.csv', '2017_08_01.csv', '2017_09_01.csv']

category_tab = [];
count_tab = [];
name_tab = [];

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
        for i in range(0,len(df)):
                find_tuples(df.iloc[i]['category_id'], df.iloc[i]['count'], df.iloc[i]['name']);

def find_tuples(category, count, name):
        find = False;
        for i in range(0, len(category_tab)):
                if category_tab[i] == category:
                        find = True;
                        count_tab[i] += count;
                        break;
        if find == False:
                category_tab.append(category)
                count_tab.append(count)
                name_tab.append(name)

def training_ranking():
        for key in keys:
                prepare_ads(key, categories)
        best_categories = [];
        for i in range(0, len(category_tab)):
                best_categories.append((count_tab[i], name_tab[i], category_tab[i]))

        best_categories = sorted(best_categories, reverse=True)
        print(best_categories[0:20])
        x = []
        y = []
        for i in range(0, 10):
                x.append(best_categories[i][1])
                y.append(best_categories[i][0])
        plt.rcParams.update({'font.size': 10})
        plt.bar(range(0,10),y)
        plt.title("Ranking kategorii treningowych", fontsize=20)
        plt.xlabel("Kategoria", fontsize=12)
        plt.ylabel("Liczba ogłosze\u0144", fontsize=12)
        plt.xticks(range(0,10), x, fontsize=10)
        plt.xticks(rotation=45)

        plt.show()
def test_ranking():
        df = ad.get_ads_test_clean("test_2017_10_01.csv")
        df = df.drop('id', 1)
        df = df.drop('region_id', 1)
        df = df[df.category_id.notnull()]
        df = df['category_id'].value_counts().reset_index()
        df.columns = ['category_id', 'count']
        df = pd.merge(df, categories, how='left', on='category_id')
        df = df[df.name.notnull()]
        x = [];
        y = [];
        for i in range(0,10):
                x.append(df.iloc[i]["name"])
                y.append(df.iloc[i]["count"])
        plt.rcParams.update({'font.size': 10})
        plt.bar(range(0,10),y)
        plt.title("Ranking kategorii testowych", fontsize=20)
        plt.xlabel("Kategoria", fontsize=12)
        plt.ylabel("Liczba ogłosze\u0144",fontsize=12)
        plt.xticks(range(0,10), x, fontsize=10)
        plt.xticks(rotation=45)
        plt.show()
ads = ad.get_ads_clean(11)
categories = categories()
training_ranking()
test_ranking()



