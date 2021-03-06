import re
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer
import DataNinja.DataReader.Config as Config
import pandas as pd
from pyMorfologik import Morfologik
from pyMorfologik.parsing import ListParser
from collections import Counter
import json

column_names = ["id", "region_id", "category_id", "subregion_id", "district_id", "city_id", "accurate_location", "user_id",
                "sorting_date", "created_at_first", "valid_to", "title", "description", "full_description", "has_phone",
                "params", "private_business", "has_person", "photo_sizes", "paidads_id_index", "paidads_valid_to",
                "predict_sold", "predict_replies", "predict_views", "reply_call", "reply_sms", "reply_chat",
                "reply_call_intent", "reply_chat_intent"]
files = ['ads_2016_11_01', 'ads_2016_12_01', 'ads_2017_01_01', 'ads_2017_02_01', 'ads_2017_03_01', 'ads_2017_04_01',
         'ads_2017_05_01', 'ads_2017_06_01', 'ads_2017_07_01', 'ads_2017_08_01', 'ads_2017_09_01']

def get_ads_from_one_month():
    for filename in files:
        file = codecs.open(Config.ADS_DATA_CATALOG + "\\" + filename, encoding='utf8')
        counter = 0
        file_write = open(Config.ADS_GENERATED_DATA_CATALOG + "\\" + filename + ".txt", "w", encoding='utf8')
        for line in file:
            line = line.replace("\n", "")
            line = line.replace("<STREET>", "")
            line = line.replace("<CITY>", "")
            line = line.replace("<POSTCODE>", "")
            line = line.replace("<URL>", "")
            line = line.replace("<PHONE>", "")
            line = line.replace("ą", "a")
            line = line.replace("ę", "e")
            line = line.replace("ó", "o")
            line = line.replace("ś", "s")
            line = line.replace("ł", "l")
            line = line.replace("ż", "z")
            line = line.replace("ź", "z")
            line = line.replace("ć", "c")
            line = line.replace("ń", "n")

            line = line.replace("Ą", "A")
            line = line.replace("Ę", "E")
            line = line.replace("Ó", "O")
            line = line.replace("Ś", "S")
            line = line.replace("Ł", "L")
            line = line.replace("Ż", "Z")
            line = line.replace("Ź", "Z")
            line = line.replace("Ć", "C")
            line = line.replace("Ń", "N")
            line = line.replace("-", " ")
            line = line.replace("{", " ")
            line = line.replace("}", " ")
            line = line.replace(".", " ")
            line = line.replace("_", " ")
            line = line.replace("/", " ")
            line = line.replace("\\", " ")
            line = line.replace("(", " ")
            line = line.replace(")", " ")
            line = line.replace("[", " ")
            line = line.replace("]", " ")
            line = line.replace(":", " ")
            line = line.replace(";", " ")
            line = line.replace("?", " ")
            line = line.replace("+", " ")
            line = line.replace("=", " ")
            line = line.replace("!", " ")
            line = line.replace("#", " ")
            line = line.replace("$", " ")
            line = line.replace("^", " ")
            line = line.replace("&", " ")
            line = line.replace("@", " ")
            line = line.replace("<", " ")
            line = line.replace(">", " ")
            #line = re.sub('[^0-9a-zA-Z", ]+', '', line)
            if line == " ":
                continue
            if line == "":
                continue
            if line != "" and not line.isspace() and counter > 0:
                file_write.write(line)
            counter += 1
        file_write.close()
        file.close()


def to_dataframe(index, nrows):
    df = pd.read_csv(Config.ADS_GENERATED_DATA_CATALOG + "\\" + files[index] + ".txt", sep=",", names=column_names, nrows=nrows)
    df = df.drop(["reply_call", "reply_sms", "reply_chat",
                "reply_call_intent", "reply_chat_intent"], axis=1)
    stemmedStr = ""
    for i in range(0, 10000):
        parser = ListParser()
        stemmer = Morfologik()
        print(i)
        stemms = stemmer.stem([df.iloc[i].full_description], parser)
        stemmedList = []
        # stemmedStr = ""
        for key in stemms:
            words = key[1].keys()
            if len(words) > 0:
                stemmedStr += list(words)[0] + " "
                # stemmedList.append(list(words)[0]
        # print(Counter(stemmedList))
        # all.append(stemmedStr)
    with open("stop-words.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words=content)
    tfidf_matrix = vectorizer.fit_transform([stemmedStr])
    feature_names = vectorizer.get_feature_names()
    dense = tfidf_matrix.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)
    s = pd.Series(df.loc[0])
    print(s[s > 0].sort_values(ascending=False)[:10])
    return df