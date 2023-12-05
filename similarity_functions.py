import pickle


def similarity_by_genres(a1: dict, a2: dict) -> float:
    genres_list1 = a1['genres'].split(', ')
    l1 = len(genres_list1)

    genres_list2 = a2['genres'].split(', ')
    l2 = len(genres_list2)

    similar = 0
    for i in range(l1):
        for j in range(l2):
            if genres_list1[i] == genres_list2[j]:
                similar += 1
    return 2 * similar / (l1 + l2)


def similarity_by_age_rating(a1: dict, a2: dict) -> float:
    age_r1 = a1['age-rating']
    age_r2 = a2['age-rating']

    age_ratings = ['G', 'PG', 'PG-13', 'R-17', 'R+']

    r1_ind = age_ratings.index(age_r1)
    r2_ind = age_ratings.index(age_r2)
    result = abs(r1_ind - r2_ind) / (len(age_ratings) - 1)
    return 1 - result


def similarity_by_studio(a1: dict, a2: dict) -> float:
    s1 = a1['studio']
    s2 = a2['studio']
    if s1 == s2:
        return 1
    else:
        return 0


def similarity_by_period(a1: dict, a2: dict) -> float:
    per1 = a1['period']
    per2 = a2['period']
    year1 = 0
    year2 = 0
    for y in range(1966, 2024):
        if str(y) in per1:
            year1 = y
        if str(y) in per2:
            year2 = y
    return 1 - abs(year1 - year2) / 55


def similarity_by_description(a1: dict, a2: dict) -> float:
    id1 = a1['id']
    id2 = a2['id']
    filename = f'description_distances_database/{id1}.pickle'
    with open(filename, 'rb') as file:
        desc_dicts = pickle.load(file)
    similarity = desc_dicts[id2]
    return similarity
