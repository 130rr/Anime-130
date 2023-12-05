import spacy
from database import *
import pickle


def all_descriptions():
    all_anime = get_all_anime()
    all_anime_dicts = [anime_to_dict(x) for x in all_anime]
    all_descns = [anime['description'] for anime in all_anime_dicts]
    return all_descns


def init_desc_sim_base():
    with open('description_distances_database.pickle', 'wb') as file:
        pickle.dump({}, file)


def write_new_desc_sim(anime_id: int, sim_list: list):
    with open('description_distances_database.pickle', 'rb') as file:
        data = pickle.load(file)
    data[anime_id] = sim_list
    with open('description_distances_database.pickle', 'wb') as file:
        pickle.dump(data, file)


def get_desc_sims():
    with open('description_distances_database.pickle', 'rb') as file:
        data = pickle.load(file)
    return data


def main():
    nlp = spacy.load("ru_core_news_lg")

    descs = all_descriptions()
    size = get_database_size()
    already_calculated = len(get_desc_sims())
    for anime_id in range(size):
        if anime_id < already_calculated:
            continue
        similarity_list = []
        doc1 = nlp(descs[anime_id])

        for i in range(size):
            percent = int(100*i/size)
            print(f'\r{anime_id + 1} of {size}: {percent}%', end=' ')

            doc2 = nlp(descs[i])
            similarity = doc1.similarity(doc2)
            similarity_list.append(similarity)
        write_new_desc_sim(anime_id, similarity_list)
        print(f'\r{anime_id + 1} of {size} done')


if __name__ == '__main__':
    main()
