import datetime


def weekday_parse(query_key):
    date = (query_key.split('_'))
    weekday = datetime.datetime(int(date[0]),int(date[1]),int(date[2])).weekday()
    return weekday