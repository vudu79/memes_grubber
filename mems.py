import json
import logging

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


def main():
    mem_info_dict = dict()
    memes_list = list()
    ua = UserAgent()

    headers = {
        "user-agent": ua.chrome
    }

    domen = "http://memesmix.net"
    print(headers["user-agent"])
    for x in range(1, 34295):
        uri = "/images/popular/alltime"
        # print(uri + " " + str(datetime.datetime.now()))
        try:
            res = requests.get(domen + uri, headers=headers)
            # print(res.text)
            if res.status_code == 200:
                print(res.status_code)
                logging.info(f'Рабатаю со страницей - {x}')
                soup = BeautifulSoup(res.text, "lxml")
                divs = soup.find_all("div", id="grid-image")
                # print(divs)
                for div in divs:
                    name = div.find("div", class_="char-name").find("a")
                    mem_info_dict["name"] = name.text if name else None
                    mem_info_dict["img"] = div.find("img").get("src")
                    buffer = mem_info_dict.copy()
                    memes_list.append(buffer)
                    mem_info_dict.clear()
                print(memes_list)
        except Exception as e:
            print(e)
            logging.error(f"Проблеммы с requests на странице с мемами - {e}")
    try:
        with open("memes.json", "w", encoding="utf-8") as f:
            json.dump(memes_list, f, indent=4, ensure_ascii=False)
        logging.info(f"В итоговом файле {len(memes_list)} записей")
    except Exception as ee:
        logging.error(f"Проблеммы с записью в файл - {ee}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="memes_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    main()
