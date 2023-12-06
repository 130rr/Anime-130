import database as db
STARTS = [
    'похожее на',
    'как',
    'вроде',
    'подобное',
]


def levenshtein_distance(a, b):
    f = [[i+j if i*j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                f[i][j] = f[i-1][j-1]
            else:
                f[i][j] = 1 + min(f[i-1][j], f[i][j-1], f[i-1][j-1])
    return f[len(a)][len(b)]


class NamesIds:
    def __init__(self):
        self.anime_dicts = db.many_anime_to_dict(db.get_all_anime())
        anime_name: list[str] = [anime['name'].strip() for anime in self.anime_dicts]
        self.anime_names = [name.lower() for name in anime_name]

    def find_id_and_distance(self, user_text: str) -> tuple[int, int]:
        user_text = user_text.lower()
        for start in STARTS:
            if start in user_text:
                index = user_text.index(start) + len(start)
                user_text = user_text[index:]

        _min = 10*100000
        anime_id = None
        for i, name in enumerate(self.anime_names):
            distance = levenshtein_distance(name, user_text)
            if distance < _min:
                _min = distance
                anime_id = i
        return anime_id, _min


def remove_seasons(main_anime: dict, anime_list: list[dict]):
    # Убираем сезоны спрашиваемого аниме
    filtered = []
    main_name: str = main_anime['name'].lower()
    for i in range(len(anime_list)):
        name = anime_list[i]['name'].lower()
        main_name = main_name.strip()
        name = name.strip()
        if main_name.startswith(name) or name.startswith(main_name):
            continue
        filtered.append(anime_list[i])

    # Убираем повторное упоминание аниме (другие сезоны)
    i = 0
    while i < len(filtered):
        new_filtered = filtered[:]
        for j in range(len(filtered)):
            if j == i:
                continue
            name1: str = filtered[i]['name'].lower().strip()
            name2: str = filtered[j]['name'].lower().strip()
            if name1 == name2 or name1.startswith(name2[:-3]) or name2.startswith(name1[:-3]):
                #print(name1, name2, 'removed')
                new_filtered[j] = {}
        while {} in new_filtered:
            new_filtered.remove({})
        filtered = new_filtered[:]
        i += 1

    return filtered
