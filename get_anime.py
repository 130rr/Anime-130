from get_links import get_request
import time

links = open('links.txt', encoding='utf-8').readlines()
for i, link in enumerate(links):
    print(i)
    time.sleep(1)
    request = get_request(link)
    html = request.text
    with open(f'Anime pages/{i}.html', 'w', encoding='utf-8') as file:
        file.write(html)
