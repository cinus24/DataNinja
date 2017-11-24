import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import DataNinja.ConfigGenerated as cg

file_path = cg.CATEGORIES_COUNT
column_name = ["index_per_day","category", "count", "parent_id", "name", "Date"]

days_count = 166
categories_count = 420

categories_top50_count = np.zeros(categories_count);
categories_top50_category_per_count = [];
categories_map = []

def read_file():
    categories = pd.read_csv(file_path,delimiter=',', engine="python", names = column_name)
    return categories

def map(categories):
    for i in range(0, categories_count):
        categories_map.append(categories.iloc[i].category);

def mining(categories):
    for day in range(0, days_count):
        categories_per_day = categories[categories_count*day:categories_count*day+categories_count]
        for index in range(0, 50):
            categories_top50_count[categories_map.index(categories_per_day.iloc[index].category)]+=1;

categories = read_file();
map(categories)
mining(categories)

queries_count_per_day = categories[['Date','count']].groupby('Date').aggregate(sum);
print(queries_count_per_day)

for i in range(0, categories_count):
    categories_top50_category_per_count.append((categories_top50_count[i], categories_map[i]))
categories_top50_category_per_count = sorted(categories_top50_category_per_count, reverse=True)
for i in range(0, categories_count):
    y = [];
    x = [];
    day_from = 0;
    day_too = 50;
    if(categories_top50_category_per_count[i][0] <= 80 and categories_top50_category_per_count[i][0] > 25 and categories_top50_category_per_count[i][0] != 0):
        #print(categories_top50_category_per_count[i])
        if(categories_top50_category_per_count[i][0] <= 80 and categories_top50_category_per_count[i][0] > 25 and categories_top50_category_per_count[i][0] != 0):

                for j in range(day_from,day_too):
                    #print(categories.loc[categories['category'] == categories_top50_category_per_count[i][1]]['count'].values[j])
                    y.append(categories.loc[categories['category'] == categories_top50_category_per_count[i][1]]['count'].values[j]/ queries_count_per_day.iloc[[j]].values[0])
                    x.append(categories.loc[categories['category'] == categories_top50_category_per_count[i][1]]['Date'].values[j])
                    #x.append(categories.loc[categories['category'] == categories_top50_category_per_count[i][1]]['Date'].values[j])
                #y = [value for value in y if not math.isnan(value)]
                #x = range(0,50)
                fig = plt.figure()
                ax = fig.add_subplot(111)
                plt.rcParams.update({'font.size': 6})
                plt.title(categories.loc[categories['category'] == categories_top50_category_per_count[i][1]]['name'].values[0])
                ax.plot(x, y, '-')
                plt.xticks(rotation=45)
                ax.grid(True)
                temp_ticks = []
                for i in range(0, len(x)):
                    if i % 3 == 0:
                        temp_ticks.append(x[i])
                    else:
                        temp_ticks.append("")
                ax.set_xticklabels(temp_ticks)
                plt.ylabel("Udzia\u0142 zapytania w stosunku do ca\u0142osci")
                plt.xlabel("Dzie\u0144")
                plt.show()

