import pandas as pd
import os
import DataNinja.DataReader.Config as Config

data_dir = Config.ADS_DATA_CATALOG

index_query = 0
index_category = 1
index_count = 2
col_names = ["query", "category", "count"]

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


def convert_count(a):
    if a is None:
        return 0
    a = a.strip('"')
    a = a.strip(',')
    a = a.strip('"')
    return int(a)


def get_ads(max_days=2):
    print("START")
    converters = {index_query: convert_query, index_category: convert_category, index_count: convert_count}
    ads_dict = dict()
    for file_index, file_name in enumerate(os.listdir(data_dir)):
        print(file_name)
        if file_index < max_days:
            p = os.path.join(data_dir, file_name)
            ads = pd.read_csv(p,delimiter='","', engine="python", header=0, quotechar='"')
            print(ads)
    # return queries_dict

get_ads()
print("STOP")
