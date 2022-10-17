# Урок 18. Домашнее задание

## Приложение, создает таблицы со связями
   Загружаю csv файл разбираю его в основной лист с словарями и на отдельные словари,
   Потом создаю таблицы со связями и записываю туда данные из словарей  
   
## Пример SQL запроса для выборки из таблиц
   SELECT sh.fk_animal_id, an.animal_id, an."name", c.color, st.outcome_subtype
   FROM shelters sh
   JOIN shelters_animal an ON an.id = sh.fk_animal_id
   JOIN animal_color c ON c.id_color = an.fk_color1
   JOIN shelters_outcome_subtype st ON st.id_outcome_subtype = sh.fk_shelters_outcome_subtype
   ORDER BY sh.fk_animal_id   

## Критерии проверки:

- [ ]  Таблицы созданы верно.
- [ ]  Связи между таблицами установлены.
- [ ]  Таблицы нормализованы по НФ(нормальной форме).
- [ ]  Колонки таблиц названы корректно и понятно.
- [ ]  В БД есть привилегии для разных пользователей.


https://github.com/GeeN33/PostgreSQL_lesson_18.git

Откройте склонированный репозиторий в PyCharm.

### создайте файл .env
в файле .env данные для подключения к БД 
host=127.0.0.1
user=*******
password=*******
db_name=db_lesson_18

### Cоздайте виртуальное окружение:

#### Простой вариант:
Pycharm может предложить вам сделать это после того, как вы откроете папку с проектом.
В этом случае после открытия папки с проектом в PyCharm
Появляется всплывающее окно, Creating virtuan envrironment c тремя полями.
В первом поле выбираем размещение папки с вирутальным окружением, как правило это папка venv
в корне проекта
Во втором поле выбираем устанавливаемый интерпритатор по умолчанию (можно оставить без изменений)
В 3 поле выбираем список зависимостей (должен быть выбран фаил requirements.txt, находящийся в корне папки проекта)

#### Если этого не произошло, тогда следует выполнить следующие действия вручную:
#### Установка виртуального окружения:
1. Во вкладке File выберите пункт Settings
2. В открывшемся окне, с левой стороны найдите вкладку с именем
вашего репозитория (Project: lesson23-and-tests)
3. В выбранной вкладке откройте настройку Python Interpreter
4. В открывшейся настройке кликните на значек ⚙ (шестеренки) 
расположенный сверху справа и выберите опцию Add
5. В открывшемся окне слева выберите Virtualenv Environment, 
а справа выберите New Environment и нажмите ОК

#### Установка зависимостей:
Для этого можно воспользоваться графическим интерфейсом PyCharm,
который вам предложит сделать это как только вы откроете файл с заданием.

Или же вы можете сделать это вручную, выполнив следующую команду в терминале:
`pip install -r requirements.txt`

#### Настройка виртуального окружения завершена!







