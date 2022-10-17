from commandes_sql import db_connect, create_tables, insert_into_not_references, insert_into_shelters_animal, insert_into_shelters
import csv

list_shelters = []
dict_shelters_animal = {}
dict_animal_type = {}
dict_animal_breed = {}
dict_animal_color = {}
dict_shelters_outcome_subtype = {}
dict_shelters_outcome_type = {}
list_tables=['animal_type', 'animal_breed', 'animal_color', 'shelters_outcome_subtype', 'shelters_outcome_type']

def parsing_csv()->None:
    """
    Загружаю csv файл разбираю его в основной лист с словарями и на отдельные словари

    """
    with open('main_animals.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
        j=0
        for row in reader:
            j += 1
            list_shelters.append(row)
            if j > 100: break
        list_shelters_animal = []
        list_animal_type = []
        list_animal_breed = []
        list_animal_color1 = []
        list_animal_color2 = []
        list_shelters_outcome_subtype = []
        list_shelters_outcome_type = []
        for animal in list_shelters:
            if animal['animal_id'] != '': list_shelters_animal.append(animal['animal_id'])
            if animal['animal_type'] != '': list_animal_type.append(animal['animal_type'])
            if animal['breed'] != '': list_animal_breed.append(animal['breed'])
            if animal['outcome_subtype'] != '': list_shelters_outcome_subtype.append(animal['outcome_subtype'])
            if animal['outcome_type'] != '': list_shelters_outcome_type.append(animal['outcome_type'])
            if animal['color1'] != '': list_animal_color1.append(animal['color1'].strip())
            if animal['color2'] != '': list_animal_color2.append(animal['color2'].strip())
        list_animal_color1.extend(list_animal_color2)
        list_shelters_animal = list(set(list_shelters_animal))
        list_animal_type = list(set(list_animal_type))
        list_animal_breed = list(set(list_animal_breed))
        list_shelters_outcome_subtype = list(set(list_shelters_outcome_subtype))
        list_shelters_outcome_type = list(set(list_shelters_outcome_type))
        list_animal_color1 = list(set(list_animal_color1))
        for i in range(len(list_shelters_animal)):
            dict_shelters_animal[list_shelters_animal[i]] = i + 1
        for i in range(len(list_animal_type)):
            dict_animal_type[list_animal_type[i]] = i + 1
        for i in range(len(list_animal_breed)):
            dict_animal_breed[list_animal_breed[i]] = i + 1
        for i in range(len(list_animal_color1)):
            dict_animal_color[list_animal_color1[i]] = i + 1
        dict_animal_color['null'] = 0
        for i in range(len(list_shelters_outcome_subtype)):
            dict_shelters_outcome_subtype[list_shelters_outcome_subtype[i]] = i + 1
        dict_shelters_outcome_subtype['null'] = 0
        for i in range(len(list_shelters_outcome_type)):
            dict_shelters_outcome_type[list_shelters_outcome_type[i]] = i + 1

def main() -> None:
    parsing_csv()
    connection = db_connect()
    create_tables(connection)
    for v in list_tables:
        insert_into_not_references(connection,
                                   dict_animal_type, dict_animal_breed,
                                   dict_animal_color,
                                   dict_shelters_outcome_subtype,
                                   dict_shelters_outcome_type, v)

    insert_into_shelters_animal(connection, dict_animal_type, dict_animal_breed, dict_animal_color,
                                dict_shelters_animal, list_shelters)

    insert_into_shelters(connection, dict_shelters_animal, dict_shelters_outcome_subtype, dict_shelters_outcome_type,
                         list_shelters)

    if connection:
        connection.close()

if __name__ == "__main__":
    main()





