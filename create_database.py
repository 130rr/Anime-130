from parsing_data import info_generator
import sqlite3


def init_database():
    # Establish a connection to the database
    open('anime_database.db', 'w')
    conn = sqlite3.connect('anime_database.db')
    cursor = conn.cursor()

    # Создаем таблицу
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Anime (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    link TEXT NOT NULL,
    age_rating TEXT NOT NULL,
    genres TEXT NOT NULL,
    period TEXT NOT NULL,
    studio TEXT NOT NULL,
    description TEXT NOT NULL
    )
    ''')

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


def add_anime(i, info, cursor):
    fields = ['name', 'link', 'age_rating', 'genres', 'period', 'studio', 'description']
    data = [i]
    for key in fields:
        field = info[key]
        data.append(field)
    # Добавляем данные (8 полей)
    cursor.execute(f'INSERT INTO anime (id, {", ".join(fields)}) VALUES (' + '?, '*7 + '?)',
                   [*data])


def fill_base():
    # Establish a connection to the database
    conn = sqlite3.connect('anime_database.db')
    cursor = conn.cursor()

    for i, info in enumerate(info_generator()):
        print(i)
        add_anime(i, info, cursor)
        # Сохраняем изменения
        conn.commit()
    # Закрываем соединение
    conn.close()


def print_all_base():
    # Establish a connection to the database
    conn = sqlite3.connect('anime_database.db')
    cursor = conn.cursor()

    # Выбираем все аниме
    cursor.execute('SELECT * FROM Anime')
    anime = cursor.fetchall()

    # Выводим результаты
    for data in anime:
        print(data[0], data[1])
        for field in data[2:]:
            print(field)
    print('-'*30)


#init_database()
#fill_base()
#print_all_base()
