import csv
import re

from pymongo import MongoClient


def read_data(db,csv_file):
    shedule = list()

    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile,  delimiter=',')
        for line in reader:
            line['Цена']= int(line['Цена'])
            shedule.append(line)
    result = concerts_collection.insert_many(shedule)
    return result



def find_cheapest(db):

    for concert in concerts_collection.find():
        concert["Цена"]= int(concert["Цена"])
    result = concerts_collection.find().sort("Цена", direction=1).limit(1)
    return list(result)


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке, например "Seconds to"),
    и вернуть их по возрастанию цены
    """
    search_result = list()
    for concert in db.find().sort("Цена", direction=1):

        search = (re.search(name, concert["Исполнитель"]))
        if search:
            search_result.append(concert)
    return search_result
    # result = db.find({"Исполнитель": name}).sort("Цена", direction=1)
    # return result


if __name__ == '__main__':
    client = MongoClient("localhost", 27017)
    concerts_db = client['admin']
    concerts_collection = concerts_db['concerts']
    #read_data(concerts_db, 'artists.csv')
    print(find_by_name("Джа", concerts_collection))

