import json
import logging

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


# сайт https://bugaga.ru
def main():
    mem_info_dict = dict()
    memes_list = list()
    ua = UserAgent()

    headers = {
        "user-agent": ua.chrome
    }
    domen = "https://bugaga.ru"
    print(headers["user-agent"])
    for x in range(1, 29):
        uri = f"/tags/%D0%BC%D0%B5%D0%BC%D1%8B/page/{x}"
        # print(uri + " " + str(datetime.datetime.now()))
        try:
            res = requests.get(domen + uri, headers=headers)
            if res.status_code == 200:
                logging.info(f'Рабатаю со страницей - {x}')
                soup = BeautifulSoup(res.text, "lxml")

                divs = soup.find_all("div", class_="w_news")
                for div in divs:
                    try:
                        pack_url = div.find("a", class_="ui-button dalee").get("href")
                        print(pack_url)
                        title = str(div.find("div", class_="w_tit").find("a").text)
                        try:
                            memes_num = int(title.split("(")[1].split(" ")[0])
                            iner_pages = memes_num // 15
                            print(iner_pages)
                            for p in range(1, iner_pages + 1):
                                part1 = pack_url.split("/interesting/")[0] + "/interesting/"
                                part2 = pack_url.split("/interesting/")[1]
                                pack_url = pack_url if p == 1 else f"{part1}page,{p},{part2}"
                                print(pack_url)
                                res = requests.get(pack_url, headers=headers)
                                if res.status_code == 200:
                                    print(res.status_code)
                                    logging.info(f'Рабатаю с ссылкой - {pack_url}')
                                    soup = BeautifulSoup(res.text, "lxml")
                                    urls = soup.find("div", class_="w_cntn").find_all("a", class_="highslide")
                                    print(len(urls))
                                    if len(urls) > 0:
                                        for a in urls:
                                            img_url = domen + a.find("img").get("src")
                                            mem_info_dict["name"] = ""
                                            mem_info_dict["img"] = img_url
                                            buffer = mem_info_dict.copy()
                                            memes_list.append(buffer)
                                            mem_info_dict.clear()

                        except Exception as ee:
                            logging.error(f"не перевелось в число количество мемов в паке {ee}")
                            memes_num = None

                    except Exception as e:
                        logging.error("проблемма с запросом на страницу мемов")

        except Exception as e:
            print(e)
            logging.error(f"Проблеммы с requests на странице со сборниками мемов - {e}")
    for x in range(0, len(memes_list)):
        print(memes_list[x]["img"])
        print("\n")
    try:
        with open("bugaga_memes.json", "w", encoding="utf-8") as f:
            json.dump(memes_list, f, indent=4)
    except Exception as ee:
        logging.error(f"Проблеммы с записью в файл - {ee}")


# сайт "http://memesmix.net"
# def main():
#     mem_info_dict = dict()
#     memes_list = list()
#     ua = UserAgent()
#
#     headers = {
#         "user-agent": ua.chrome
#     }
#
#     domen = "http://memesmix.net"
#     print(headers["user-agent"])
#     for x in range(1, 34295):
#         uri = "/images/popular/alltime"
#         # print(uri + " " + str(datetime.datetime.now()))
#         try:
#             res = requests.get(domen + uri, headers=headers)
#             # print(res.text)
#             if res.status_code == 200:
#                 print(res.status_code)
#                 logging.info(f'Рабатаю со страницей - {x}')
#                 soup = BeautifulSoup(res.text, "lxml")
#                 divs = soup.find_all("div", id="grid-image")
#                 # print(divs)
#                 for div in divs:
#                     name = div.find("div", class_="char-name").find("a")
#                     mem_info_dict["name"] = name.text if name else None
#                     mem_info_dict["img"] = div.find("img").get("src")
#                     buffer = mem_info_dict.copy()
#                     memes_list.append(buffer)
#                     mem_info_dict.clear()
#                 print(memes_list)
#         except Exception as e:
#             print(e)
#             logging.error(f"Проблеммы с requests на странице с мемами - {e}")
#     try:
#         with open("memes.json", "w", encoding="utf-8") as f:
#             json.dump(memes_list, f, indent=4, ensure_ascii=False)
#         logging.info(f"В итоговом файле {len(memes_list)} записей")
#     except Exception as ee:
#         logging.error(f"Проблеммы с записью в файл - {ee}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="memes_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    main()
