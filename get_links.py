import requests
import time
HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

http_proxy = "https://85.26.146.169:80"
proxies = {
              "http": http_proxy,
            }
list_url_start = 'https://shikimori.one/animes/kind/tv,ova,ona/status/ongoing,released/page/'
list_url_end = '?score=6'


def get_request(url):
    return requests.get(url, headers=HEADERS, proxies=proxies)


def main():
    for i in range(350):
        print(i)
        list_url = list_url_start + str(i) + list_url_end
        r = get_request(list_url)
        text = r.text
        with open(f'Anime list/{i+1}.txt', 'w', encoding='utf-8') as file:
            file.write(text)
        time.sleep(0.1)


if __name__ == '__main__':
    main()
