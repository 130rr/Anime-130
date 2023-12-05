from bs4 import BeautifulSoup

with open('links.txt', 'w') as file:
    for i in range(1, 312):
        if i % 25 == 0: print(i)
        file1 = open(f'Anime list/{i}.txt', encoding='utf-8')
        text = file1.read()
        soup = BeautifulSoup(text, 'html.parser')
        tegs = soup.find_all('a', attrs={'class':"cover anime-tooltip"})
        for teg in tegs:
            teg_text = str(teg)
            href_ind = teg_text.find('href=') + 6
            link_end_ind = teg_text.find('"', href_ind)
            link = teg_text[href_ind:link_end_ind]
            file.write(link+'\n')
