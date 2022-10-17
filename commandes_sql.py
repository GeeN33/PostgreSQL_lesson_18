import psycopg2
import os
from dotenv import load_dotenv, find_dotenv

list_tables_create=['animal_type', 'animal_breed', 'animal_color', 'shelters_outcome_subtype', 'shelters_outcome_type','shelters_animal','shelters']

def db_connect():
    """
     Соединяется с базой данных
    :return: соединение
    """
    try:
        load_dotenv(find_dotenv())
        connection = psycopg2.connect(host= os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'), database=os.getenv('db_name'))
        connection.autocommit = True
        print('connection')
        return connection

    except Exception as ex:
        print(ex)
        return False

def request(connection, command) -> None:
    """
    Отправляет SQL команды в базу данных
    :param Соединение:
    :param SQL команды:
    :return:
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(command)
            return cursor.fetchall()
    except Exception as ex:
        return ex

def print_rez(rez,name_table) -> None:
    """
     Выводит таблицу
    :param rez:Данные из базы
    """
    if type(rez) == list:
        for r in rez:
            print(r)
    elif str(rez) == 'no results to fetch':
        print('create_table: '+ name_table)
    else: print(rez)

def create_tables(connection):
    """
    Создаёт таблицы по циклу, имена таблиц в листе
    """
    for v in list_tables_create:
        command = create_table(v)
        rez = request(connection, command)
        print_rez(rez,v)

def create_table(name_table:str):
    """
     Команды для создания таблиц
    :param name_table: таблица
    """
    match name_table:
        case 'animal_type':
            command = """
            CREATE TABLE IF NOT EXISTS animal_type
            (
            id_type serial PRIMARY KEY,
            type varchar(150) NOT NULL      
            )
            """
            return  command
        case 'animal_breed':
            command = """
            CREATE TABLE IF NOT EXISTS animal_breed
            (
            id_breed serial PRIMARY KEY,
            breed varchar(150) NOT NULL      
            )
            """
            return command
        case 'animal_color':
            command = """
            CREATE TABLE IF NOT EXISTS animal_color
            (
            id_color serial PRIMARY KEY,
            color varchar(150) NOT NULL      
            )
            """
            return command
        case 'shelters_animal':
            command = """
            CREATE TABLE IF NOT EXISTS shelters_animal
            (
            id serial PRIMARY KEY,
            animal_id varchar(150) NOT NULL, 
            fk_animal_type integer REFERENCES animal_type(id_type),
            name varchar(150),
            fk_breed integer REFERENCES animal_breed(id_breed),
            fk_color1 integer REFERENCES animal_color(id_color),
            fk_color2 integer REFERENCES animal_color(id_color),
            date_of_birth varchar(150) NOT NULL     
            )
            """
            return command
        case 'shelters_outcome_subtype':
            command = """
            CREATE TABLE IF NOT EXISTS shelters_outcome_subtype
            (
            id_outcome_subtype serial PRIMARY KEY,
            outcome_subtype varchar(150) NOT NULL      
            )
            """
            return command
        case 'shelters_outcome_type':
            command = """
             CREATE TABLE IF NOT EXISTS shelters_outcome_type
             (
             id_outcome_type serial PRIMARY KEY,
             outcome_type varchar(150) NOT NULL      
             )
             """
            return command
        case 'shelters':
            command = """
                  CREATE TABLE IF NOT EXISTS shelters
                  (
                  id serial PRIMARY KEY,
                  fk_animal_id integer REFERENCES shelters_animal(id),
                  fk_shelters_outcome_subtype integer REFERENCES shelters_outcome_subtype(id_outcome_subtype),
                  fk_shelters_outcome_type integer REFERENCES shelters_outcome_type(id_outcome_type),
                  outcome_month integer NOT NULL,
                  outcome_year integer NOT NULL,
                  age_upon_outcome varchar(150) NOT NULL               
                  )
                  """
            return command

def color_corect(dict_animal_color:dict,color:str):
    """
     Коррекция цвета, удаление пробелов
    :param dict_animal_color:
    :param color:
    :return:
    """
    if color != '':
        return dict_animal_color[color.strip()]
    else:return '0'

def name_corect(name:str):
    """
    Коррекция имени,  удаление не нужных символов
    :param name:
    :return:
    """
    if name != '':
        return name.replace("'", '')
    else:return ''

def outcome_subtype_corect(name:str):
    """
    Коррекция, удаление не нужных символов
    :param name:
    :return:
    """
    if name != '':
        return name
    else:return 'null'

def list_return_dict(animal_id:str, list_shelters:list):
    """
     Возвращает справочник из общего листа по  animal_id
    :param animal_id:
    :param list_shelters:
    :return:
    """
    for l in list_shelters:
        if animal_id == l['animal_id']:
            return l

    return {}

def insert_into_not_references(connection, dict_animal_type:dict, dict_animal_breed:dict, dict_animal_color:dict, dict_shelters_outcome_subtype:dict, dict_shelters_outcome_type:dict, name_table:str):
    """
     Заполнение таблиц animal_type, animal_breed, animal_color, shelters_outcome_subtype, shelters_outcome_type
    :param connection:
    :param dict_animal_type:
    :param dict_animal_breed:
    :param dict_animal_color:
    :param dict_shelters_outcome_subtype:
    :param dict_shelters_outcome_type:
    :param name_table:
    :return:
    """

    match name_table:

        case 'animal_type':
            try:
                with connection.cursor() as cursor:
                    for v in dict_animal_type:
                        cursor.execute(f"""
                        INSERT INTO animal_type (type)
                         VALUES ('{v}')
                        """)

                    print('Заполнена таблица  animal_type')

            except Exception as ex:
                print(ex)
        case 'animal_breed':
            try:
                with connection.cursor() as cursor:
                    for v in dict_animal_breed:
                        cursor.execute(f"""
                                INSERT INTO animal_breed (breed)
                                 VALUES ('{v}')
                                """)

                    print('Заполнена таблица  animal_breed')

            except Exception as ex:
                print(ex)
        case 'animal_color':
            try:
                with connection.cursor() as cursor:
                    for k,v in dict_animal_color.items():
                        cursor.execute(f"""
                             INSERT INTO animal_color (id_color, color)
                              VALUES ('{v}','{k}')
                             """)

                    print('Заполнена таблица  animal_color')

            except Exception as ex:
                print(ex)
        case 'shelters_outcome_subtype':
            try:
                with connection.cursor() as cursor:
                    for k, v in dict_shelters_outcome_subtype.items():
                        cursor.execute(f"""
                                     INSERT INTO shelters_outcome_subtype (id_outcome_subtype, outcome_subtype)
                                      VALUES ('{v}','{k}')
                                     """)

                    print('Заполнена таблица shelters_outcome_subtype')

            except Exception as ex:
                print(ex)
        case 'shelters_outcome_type':
            try:
                with connection.cursor() as cursor:
                    for v in dict_shelters_outcome_type:
                        cursor.execute(f"""
                                     INSERT INTO shelters_outcome_type (outcome_type)
                                      VALUES ('{v}')
                                     """)

                    print('Заполнена таблица shelters_outcome_type')

            except Exception as ex:
                print(ex)

def insert_into_shelters_animal(connection,dict_animal_type: dict, dict_animal_breed: dict,dict_animal_color: dict,dict_shelters_animal: dict,list_shelters:list):
    """
     Заполнение таблицы shelters_animal
    :param connection:
    :param dict_animal_type:
    :param dict_animal_breed:
    :param dict_animal_color:
    :param dict_shelters_animal:
    :param list_shelters:
    :return:
    """
    try:
        with connection.cursor() as cursor:

            for k, v in dict_shelters_animal.items():
                rez = list_return_dict(k, list_shelters)
                q = f"""
                    INSERT INTO shelters_animal (id, animal_id, fk_animal_type, name, fk_breed, fk_color1, fk_color2, date_of_birth)

                    VALUES ('{v}','{k}','{dict_animal_type[rez['animal_type']]}','{name_corect(rez['name'])}','{dict_animal_breed[rez['breed']]}','{color_corect(dict_animal_color, rez['color1'])}','{color_corect(dict_animal_color, rez['color2'])}','{rez['date_of_birth']}')
                    """

                cursor.execute(q)
            print('Заполнена таблица shelters_animal')
    except Exception as ex:
        print(ex)

def insert_into_shelters(connection,dict_shelters_animal: dict,dict_shelters_outcome_subtype: dict,dict_shelters_outcome_type: dict,list_shelters:list):
    """
     Заполнение таблиц shelters
    :param connection:
    :param dict_shelters_animal:
    :param dict_shelters_outcome_subtype:
    :param dict_shelters_outcome_type:
    :param list_shelters:
    :return:
    """
    try:
        with connection.cursor() as cursor:
            for v in list_shelters:
                q = f"""
                    INSERT INTO shelters (fk_animal_id, fk_shelters_outcome_subtype, fk_shelters_outcome_type, outcome_month, outcome_year, age_upon_outcome)

                    VALUES ('{dict_shelters_animal[v['animal_id']]}','{dict_shelters_outcome_subtype[outcome_subtype_corect(v['outcome_subtype'])]}','{dict_shelters_outcome_type[v['outcome_type']]}','{v['outcome_month']}','{v['outcome_year']}','{v['age_upon_outcome']}')
                    """
                cursor.execute(q)
            print('Заполнена таблица shelters')
    except Exception as ex:
        print(ex)


