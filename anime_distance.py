import pickle
from database import *
import similarity_functions as sf

fields_aspects = {
    'genre': 3,
    'age-rating': 3,
    'studio': 1,
    'period': 2,
    'description': 9
}


def anime_similarity(id1, id2):
    anime1 = get_anime_dict(id1)
    anime2 = get_anime_dict(id2)
    aspects_sum = sum(fields_aspects.values())
    similarity = 0
    similarity += sf.similarity_by_period(anime1, anime2) * fields_aspects['period']
    similarity += sf.similarity_by_studio(anime1, anime2) * fields_aspects['studio']
    similarity += sf.similarity_by_genres(anime1, anime2) * fields_aspects['genre']
    similarity += sf.similarity_by_age_rating(anime1, anime2) * fields_aspects['age-rating']
    similarity += sf.similarity_by_description(anime1, anime2) * fields_aspects['description']
    similarity /= aspects_sum
    return similarity


def get_similar(anime_id, n=10):
    sim_list = []
    for i in range(get_database_size()):
        if i == anime_id:
            continue
        print('\r', anime_id, i, end='')
        similarity = anime_similarity(anime_id, i)
        sim_list.append([i, similarity])
    sim_list.sort(key=lambda x: x[1], reverse=True)
    print()
    return sim_list[:n]


def only_ids_from_similar(sim_list):
    return [anime[0] for anime in sim_list]


def init_database():
    try:
        open('10recommendation.pickle')
    except FileNotFoundError:
        with open('10recommendation.pickle', 'wb') as file:
            pickle.dump([], file)


if __name__ == '__main__':
    init_database()
    for i in range(get_database_size()):
        with open('10recommendation.pickle', 'rb') as file:
            data = pickle.load(file)
        if len(data) > i:
            continue
        similar = get_similar(i)
        similar_ids = only_ids_from_similar(similar)
        data.append(similar_ids)
        with open('10recommendation.pickle', 'wb') as file:
            pickle.dump(data, file)
