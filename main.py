import os
import requests
import json
from bs4 import BeautifulSoup as BS


class Parsing:
    def __init__(self, page):
        self.page = page

    def get_content(self):
        r = requests.get(f"https://kun.uz/uz/news/category/{self.page}")
        html = BS(r.content, 'html.parser')

        json_data = []
        post_id = 1
        for el in html.select("#news-list .news"):
            img = el.select_one(".news__img > img")
            title = el.select_one(".news__title").get_text(strip=True)
            pub_date = el.select_one(".news-meta > span").get_text(strip=True)
            img_link = img["src"]
            json_data.append({
                "title": title,
                "pub_date": pub_date
            })
            os.makedirs(f'date/{self.page}/images', exist_ok=True)
            with open(f"date/{self.page}/images/img_{post_id}.png", mode="wb") as f:
                img_res = requests.get(f"{img_link}")
                f.write(img_res.content)
            os.makedirs(f"date/{self.page}/images", exist_ok=True)
            with open(f"date/{self.page}/date.json", mode="w", encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            post_id += 1

    def __repr__(self):
        print("success")


jahon = Parsing("jahon")
jahon.get_content()
