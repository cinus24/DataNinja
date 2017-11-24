import pandas as pd
import matplotlib.pyplot as plt
import DataNinja.DataReader.AdsReader as AdsReader
from DataNinja.Utils.Types import represents_float
import scipy
import scipy.stats


def count_views():
    ads = AdsReader.get_ads_clean(max_months=11)
    views_clean = []
    for month in ads:
        views = ads[month]["views"].dropna()
        for x in views:
            if isinstance(x, float):
                views_clean.append(x)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n, bins, patches = ax.hist(views_clean)

    labels = n

    for rect, label in zip(patches, labels):
        height = rect.get_height()
        if label == 0.0:
            label = ""
        else:
            label = int(label)
        ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')
    ax.set_xlabel("Liczba wy\u015Bwietle\u0144")
    ax.set_ylabel("Liczba og\u0142osze\u0144")
    ax.grid(True)
    plt.show()


def count_replies():
    ads = AdsReader.get_ads_clean(max_months=11)
    replies_clean = []
    for month in ads:
        replies = ads[month]["replies"].dropna()
        for x in replies:
            if isinstance(x, float):
                replies_clean.append(x)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n, bins, patches = ax.hist(replies_clean)

    labels = n

    for rect, label in zip(patches, labels):
        height = rect.get_height()
        if label == 0.0:
            label = ""
        else:
            label = int(label)
        ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')
    ax.set_xlabel("Liczba odpowiedzi")
    ax.set_ylabel("Liczba og\u0142osze\u0144")
    ax.grid(True)
    plt.show()


def count_sold():
    ads = AdsReader.get_ads_clean(max_months=11)
    sold_clean = []
    for month in ads:
        sold = ads[month]["sold"].dropna()
        for x in sold:
            if x == "f":
                sold_clean.append(0)
            elif x == "t":
                sold_clean.append(1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n, bins, patches = ax.hist(sold_clean, [0, 0.5, 1])

    labels = n

    for rect, label in zip(patches, labels):
        height = rect.get_height()
        if label == 0.0:
            label = ""
        else:
            label = int(label)
        ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')
    ax.set_xlabel("Liczba sprzedanych")
    ax.set_ylabel("Liczba og\u0142osze\u0144")
    ax.set_xticklabels(["", "", "nie", "", "", "tak"])
    ax.grid(True)
    plt.show()


def calculate_correlation():
    ads = AdsReader.get_ads_clean(max_months=11)
    views_clean = []
    sold_clean = []
    for month in ads:
        views_sold = ads[month][["replies", "views"]].dropna()
        views = views_sold["views"]
        sold = views_sold["replies"]
        counter = 0
        for x in views:
            if isinstance(x, float):
                if isinstance(sold.iloc[counter], float):
                    sold_clean.append(sold.iloc[counter])
                    views_clean.append(x)
            counter += 1
    print(scipy.stats.pearsonr(views_clean, sold_clean))
    plt.plot(views_clean, sold_clean, 'ro')
    plt.grid(True)
    plt.xlabel("Liczba wy\u015Bwietle\u0144")
    plt.ylabel("Liczba odpowiedzi")
    plt.show()


def calculate_correlation_categories():
    ads = AdsReader.get_ads_clean(max_months=11)
    categories = ["Komputery stacj.", "Laptopy", "Monitory"]
    cat_15 = 7267
    cat_207 = 18471
    cat_32 = 2234
    sum_15 = 0
    sum_207 = 0
    sum_32 = 0
    for month in ads:
        cat_sold = ads[month][["category_id", "views"]].dropna()
        group_sold = cat_sold.groupby("category_id")
        keys = group_sold.groups.keys()
        if 1197 in keys:
            group = group_sold.get_group(1197)
            for x in group["views"]:
                if isinstance(x, float):
                    sum_15 += x
        if '1197' in keys:
            group = group_sold.get_group('1197')
            for x in group["views"]:
                if isinstance(x, float):
                    sum_15 += x
        if 1199 in keys:
            group = group_sold.get_group(1199)
            for x in group["views"]:
                if isinstance(x, float):
                    sum_207 += x
        if '1199' in keys:
            group = group_sold.get_group('1199')
            for x in group["views"]:
                if isinstance(x, float):
                    sum_207 += x
        if 1201 in keys:
            group = group_sold.get_group(1201)
            for x in group["views"]:
                if isinstance(x, float):
                    sum_32 += x
        if '1201' in keys:
            group = group_sold.get_group('1201')
            for x in group["views"]:
                if isinstance(x, float):
                    sum_32 += x
    div = [sum_15*100/cat_15, sum_207*100/cat_207, sum_32*100/cat_32]
    print(div)
    plt.bar(categories, div)
    plt.grid(True)
    plt.xlabel("Kategoria")
    plt.ylabel("Stosunek liczby wy\u015Bwietlonych do liczby zapyta\u0144 [%]")
    plt.show()

calculate_correlation_categories()



