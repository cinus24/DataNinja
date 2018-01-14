import DataNinja.DataReader.NewAdsReader as adsReader
from sklearn.naive_bayes import GaussianNB
import datetime
import pandas as pd

def get_state(state):
    if pd.isnull(state):
        return 0
    elif "state" in state:
        if "new" in state:
            return 1
        else:
            return 2
    else:
        return 0

def bayes():
    X_predicted = []
    Y_predicted = []
    X = []
    Y = []

    for file_index in range(0, len(adsReader.files)):
        print(file_index)

        df = adsReader.to_dataframe(file_index)
        df = df.drop(["id", "subregion_id", "district_id", "city_id", "accurate_location", "user_id","description", "full_description", "has_phone",
                     "private_business", "title", "photo_sizes", "has_person", "paidads_id_index", "paidads_valid_to", "created_at_first","valid_to"], axis=1)

        df = df[0:50000]

        for i in range(0, 18000):
            day = adsReader.files[file_index][4:]
            day_of_file = datetime.datetime.strptime(day, '%Y_%m_%d')
            sorting_date = df.iloc[i]['sorting_date'][:10]
            sorting_date = datetime.datetime.strptime(sorting_date, '%Y %m %d')

            state = get_state(df.iloc[i]['params'])

            train_element = [df.iloc[i]['region_id'], df.iloc[i]['category_id'], (day_of_file - sorting_date).days,
                             state]

            predict_element = []
            predict_element.append(df.iloc[i]['predict_views'])

            X.append(train_element)
            Y.append(predict_element)

        for i in range(18000,20000):
            day = adsReader.files[file_index][4:]
            day_of_file = datetime.datetime.strptime(day, '%Y_%m_%d')
            sorting_date = df.iloc[i]['sorting_date'][:10]
            sorting_date = datetime.datetime.strptime(sorting_date, '%Y %m %d')

            state = get_state(df.iloc[i]['params'])

            train_element = [df.iloc[i]['region_id'], df.iloc[i]['category_id'], (day_of_file - sorting_date).days,
                             state]
            X_predicted.append(train_element)

            Y_predicted.append(df.iloc[i]['predict_views'])

        del df


    clf = GaussianNB()
    clf.fit(X, Y)
    predicted = clf.predict(X_predicted)

    count = 0
    for i in range(0, len(predicted)):
        if predicted[i] == Y_predicted[i]:
            count += 1
    print(count / len(predicted))


bayes()
