from bs4 import BeautifulSoup


def info(i):
    adict = {}
    file1 = open(f'Anime pages/{i}.html', encoding='utf-8')
    text = file1.read()
    soup = BeautifulSoup(text, 'html.parser')

    title = soup.find('h1')
    try:
        descr = soup.find('div', attrs={'class': 'b-text_with_paragraphs'}).text
    except AttributeError:
        descr = 'Not Found'
    genres = soup.find_all('span', attrs={'class': 'genre-ru'})
    try:
        studio = soup.find('img', attrs={'class': 'studio-logo'}).get('alt')
    except AttributeError:
        studio = 'Not Found'

    genres_list = []
    for genre in genres:
        genres_list.append(genre.text)
    genres = ', '.join(genres_list)

    spans = soup.find_all('span', attrs={'data-direction': 'right'})
    try:
        period, age_r = map(lambda x: x.text, spans)
    except ValueError:
        period = 'Not Found'
        try:
            age_r = soup.find('span', attrs={'data-direction': 'right'}).text
        except AttributeError:
            age_r = 'Not Found'

    with open('links.txt', encoding='utf-8') as links_file:
        for j, line in enumerate(links_file.readlines()):
            if i == j:
                link = line[:-1]
                break
        else:
            link = 'Not Found'

    adict['name'] = title.text.split('/')[0]
    adict['link'] = link
    adict['age_rating'] = age_r
    adict['genres'] = genres
    adict['period'] = period
    adict['studio'] = studio
    adict['description'] = descr
    return adict


def info_generator():
    for i in range(5030):
        if i == 61:
            continue
        data = info(i)
        if list(data.values()).count('Not Found') > 0:
            continue
        yield data


if __name__ == '__main__':
    for anime_info in info_generator():
        print(anime_info)
