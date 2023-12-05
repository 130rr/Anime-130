import sqlite3


def get_all_anime():
    conn = sqlite3.connect('anime_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Anime')
    anime = cursor.fetchall()
    return anime


def get_one_anime(n):
    conn = sqlite3.connect('anime_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Anime')
    anime = None
    for _ in range(n+1):
        anime = cursor.fetchone()
    return anime


def get_database_size():
    conn = sqlite3.connect('anime_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Anime')
    return len(cursor.fetchall())


def anime_to_dict(anime):
    res = {
        'id': anime[0],
        'name': anime[1],
        'link': anime[2],
        'age-rating': anime[3],
        'genres': anime[4],
        'period': anime[5],
        'studio': anime[6],
        'description': anime[7]
    }
    return res


def many_anime_to_dict(anime_list):
    return [anime_to_dict(x) for x in anime_list]


def get_anime_dict(n):
    anime_info = get_one_anime(n)
    anime_dict = anime_to_dict(anime_info)
    return anime_dict


class Base:
    def __init__(self):
        self.animes = get_all_anime()
        self.anime_dicts = many_anime_to_dict(self.animes)

    def get_anime_dict(self, n):
        return self.anime_dicts[n]
