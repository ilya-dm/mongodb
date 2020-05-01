import csv
import re

from pymongo import MongoClient


def read_data(db, csv_file):
    schedule = list()

    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile, delimiter=',')
        for line in reader:
            line['Цена'] = int(line['Цена'])
            schedule.append(line)
    result = concerts_collection.insert_many(schedule)
    return result


def find_cheapest(db):
    result = concerts_collection.find().sort("Цена", direction=1).limit(1)
    return list(result)


def find_by_name(name, db):
    regex = re.compile(name, re.IGNORECASE)
    result = list(db.find({"Исполнитель": regex}).sort("Цена", direction=1))
    return result


if __name__ == '__main__':
    client = MongoClient("localhost", 27017)
    concerts_db = client['admin']
    concerts_collection = concerts_db['concerts']
    #read_data(concerts_db, 'artists.csv')
    print(find_by_name("jon", concerts_collection))
