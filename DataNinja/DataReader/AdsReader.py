import pandas as pd
import os
import re
import codecs
from pandas.util.testing import DataFrame
import DataNinja.DataReader.Config as Config

data_dir = Config.ADS_DATA_CATALOG

index_query = 0
index_category = 1
index_count = 2
col_names = ["id", "region_id", "category_id", "sold", "replies", "views"]

def represents_int(s):
    regex = "^[0-9]+$"
    regex_test = re.compile(regex)
    if regex_test.match(s):
        return True
    return False


def get_ads_from_one_month(path, progress=False):
    file = codecs.open(Config.ADS_DATA_CATALOG + "/" + path, encoding='utf8')
    lines = []
    count = 0
    for line in file:
        line = line.strip()
        line = line.replace("\"\"", "")
        line = re.sub('[a-zA-Z],[a-zA-Z]]', '', line)
        line = line.split(",")
        if len(line) > 7:
            new_line_stats = []
            new_line_info = []
            is_stats = False
            is_info = True
            for i in range(0, 4):
                if not represents_int(line[i][1:-1]):
                    is_info = False
                    break
            if is_info:
                new_line_info += line[0:3]
            for l in line:
                if l == "\"f\"" or l == "\"t\"":
                    is_stats = True
                if is_stats:
                    l = l.replace("\"", "")
                    new_line_stats.append(l)
            if len(new_line_stats) > 8:
                new_line_stats = new_line_stats[-8:]
                new_line_stats = new_line_stats[0:3]
            if is_stats or is_info:
                if len(new_line_info) > 0:
                    for i in range(0, 3):
                        new_line_info[i] = new_line_info[i].replace("\"", "")
                    lines.append(new_line_info)
                    count += 0.5
                if len(new_line_stats) > 0:
                    count += 0.5
                    size = len(lines)
                    lines[size-1] += new_line_stats
                if progress:
                    print(count)
    ads = DataFrame(lines, columns=col_names)
    return ads


#NOTE: high RAM usage - may not work for large datasets
def get_ads(max_months=2, progress=False):
    ads_dict = dict()
    for file_index, file_name in enumerate(os.listdir(data_dir)):
        if file_index < max_months:
            ads = get_ads_from_one_month(file_name, progress)
            key = file_name
            ads_dict[key] = ads
    return ads_dict
