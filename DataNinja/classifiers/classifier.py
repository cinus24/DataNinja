import DataNinja.DataReader.NewAdsReader as adsReader
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import datetime
import pandas as pd

'''
wiek         0.033971
centymetr    0.031818
być          0.030125
stan         0.029283
tanio          0.029280
cena         0.029252
rozmiar      0.028540
sprzedać     0.028243
ocean        0.028177
gratis          0.027807
'''

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

def get_day(file_day, sorting_day):
    day = file_day[4:]
    day_of_file = datetime.datetime.strptime(day, '%Y_%m_%d')
    sorting_date = sorting_day[:10]
    sorting_date = datetime.datetime.strptime(sorting_date, '%Y %m %d')
    return (day_of_file - sorting_date).days

def views_accurency(predicted, Y_predicted_views):
    count = 0
    for i in range(0, len(predicted)):
        if 0 <= predicted[i] < 1 and 0 <= Y_predicted_views[i] < 1:
            count += 1
        elif 1 <= predicted[i] < 3 and 1 <= Y_predicted_views[i] < 3:
            count += 1
        elif 3 <= predicted[i] < 10 and 3 <= Y_predicted_views[i] < 10:
            count += 1
        elif 10 <= predicted[i] < 35 and 10 <= Y_predicted_views[i] < 35:
            count += 1
        elif predicted[i] > 35 and Y_predicted_views[i] > 35:
            count += 1

    print("views accuracy:")
    print(count / len(predicted))

def replies_accurency(predicted, Y_predicted_replies):
    count = 0
    for i in range(0, len(predicted)):
        if 0 <= predicted[i] < 1 and 0 <= Y_predicted_replies[i] < 1:
            count += 1
        elif 1 <= predicted[i] < 3 and 1 <= Y_predicted_replies[i] < 3:
            count += 1
        elif 3 <= predicted[i] < 6 and 3 <= Y_predicted_replies[i] < 6:
            count += 1
        elif predicted[i] > 6 and Y_predicted_replies[i] > 6:
            count += 1
    print("replies accuracy:")
    print(count / len(predicted))

def sold_accurency(predicted, Y_predicted_sold):
    count = 0
    for i in range(0, len(predicted)):
        if predicted[i] == Y_predicted_sold[i]:
            count += 1
    print("sold accuracy:")
    print(count / len(predicted))

def classifier():
    X_predicted = []  # dane z zbioru do wyznaczenia
    Y_predicted_views = []
    Y_predicted_replies = []
    Y_predicted_sold = []

    X = [] # dane z zbioru treningowego
    Y_views = []
    Y_replies = []
    Y_sold = []

    nrows = 10000

    for file_index in range(0, len(adsReader.files)):
        print(file_index)

        df = adsReader.to_dataframe(file_index, nrows)
        df = df.drop(["id", "subregion_id", "district_id", "city_id", "accurate_location", "user_id","description", "full_description", "has_phone",
                     "private_business", "title", "photo_sizes", "has_person", "paidads_id_index", "paidads_valid_to", "created_at_first","valid_to"], axis=1)

        df = df[0:nrows]

        for i in range(0, int(nrows*9/10)):

            days = get_day(adsReader.files[file_index], df.iloc[i]['sorting_date'])
            state = get_state(df.iloc[i]['params'])

            train_element = [df.iloc[i]['region_id'], df.iloc[i]['category_id'], days,
                             state]

            predict_views = []
            predict_views.append(df.iloc[i]['predict_views'])

            predict_replies = []
            predict_replies.append(df.iloc[i]['predict_replies'])

            predict_sold = []

            if df.iloc[i]['predict_sold'] == 'f':
                sold = 0
            else:
                sold = 1
            predict_sold.append(sold)

            X.append(train_element)
            Y_views.append(predict_views)
            Y_replies.append(predict_replies)
            Y_sold.append(predict_sold)

        for i in range(int(nrows*9/10), nrows):
            days = get_day(adsReader.files[file_index], df.iloc[i]['sorting_date'])
            state = get_state(df.iloc[i]['params'])

            train_element = [df.iloc[i]['region_id'], df.iloc[i]['category_id'], days,
                             state]
            X_predicted.append(train_element)

            Y_predicted_views.append(df.iloc[i]['predict_views'])
            Y_predicted_replies.append(df.iloc[i]['predict_replies'])
            if df.iloc[i]['predict_sold'] == 'f':
                Y_predicted_sold.append(0)
            else:
                Y_predicted_sold.append(1)

        del df

    clf = GaussianNB()
    #clf = LogisticRegression()
    #clf = KNeighborsClassifier(n_neighbors=3)
    #clf = tree.DecisionTreeClassifier()
    clf.fit(X, Y_views)
    predicted = clf.predict(X_predicted)
    views_accurency(predicted, Y_predicted_views)

    clf = GaussianNB()
    #clf = LogisticRegression()
    #clf = KNeighborsClassifier(n_neighbors=3)
    #clf = tree.DecisionTreeClassifier()
    clf.fit(X, Y_replies)
    predicted = clf.predict(X_predicted)
    replies_accurency(predicted, Y_predicted_replies)

    clf = GaussianNB()
    #clf = LogisticRegression()
    #clf = KNeighborsClassifier(n_neighbors=3)
    #clf = tree.DecisionTreeClassifier()
    clf.fit(X, Y_sold)
    predicted = clf.predict(X_predicted)
    sold_accurency(predicted, Y_predicted_sold)


classifier()
