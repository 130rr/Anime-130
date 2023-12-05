import pickle
from database import *


def get_similar_ids(anime_id):
    with open('10recommendation.pickle', 'rb') as file:
        data = pickle.load(file)
    return data[anime_id]


def info_about_anime(anime_id):
    return get_anime_dict(anime_id)


if __name__ == '__main__':
    similar = get_similar_ids(45)
    print(similar)
    for anime_id in similar:
        print(info_about_anime(anime_id))
