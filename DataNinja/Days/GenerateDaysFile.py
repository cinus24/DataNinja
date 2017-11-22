import pandas as pd
import os
import DataNinja.DataReader.Config as Config

data_dir = Config.QUERIES_DATA_CATALOG

def generate_days():
    file_names = [];
    for file_name in os.listdir(data_dir):
        file_names.append(file_name[15:len(file_name)-4])
    d = {'day': file_names}
    df = pd.DataFrame(data=d)
    with open('Days.csv', 'a') as f:
        df.to_csv(f, header=False)

generate_days()