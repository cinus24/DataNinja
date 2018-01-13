import re
import codecs
import DataNinja.DataReader.Config as Config
import pandas as pd

column_names = ["id","region_id","category_id","subregion_id","district_id","city_id","accurate_location","user_id","sorting_date","created_at_first","valid_to","title","description","full_description","has_phone","params","private_business","has_person","photo_sizes","paidads_id_index","paidads_valid_to","predict_sold","predict_replies","predict_views","reply_call","reply_sms","reply_chat","reply_call_intent","reply_chat_intent"]

def get_ads_from_one_month():
    path = 'ads_2016_12_01'
    file = codecs.open(Config.ADS_DATA_CATALOG + "\\" + path, encoding='utf8')
    counter = 0
    file_write = open("ads_2016_12_01.txt", "w", encoding='utf8')
    for line in file:
        line = line.replace("\n", "")
        line = line.replace("<STREET>", "")
        line = line.replace("<CITY>", "")
        line = line.replace("<POSTCODE>", "")
        line = line.replace("<URL>", "")
        line = re.sub('[^0-9a-zA-Z",.?:;{}\-_+=!@#$%^&* ąęółżź()[]/\\\]+', '', line)
        if line != "" and not line.isspace() and counter > 0:
            file_write.write(line)
        counter += 1
    file_write.close()
    file.close()

def to_dataframe():
    df = pd.read_csv('ads_2016_12_01.txt', sep=",", header=None, names=column_names)
    print(df.iloc[0].full_description)

get_ads_from_one_month()
to_dataframe()