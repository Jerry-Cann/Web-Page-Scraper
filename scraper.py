import string
import requests
import os
from bs4 import BeautifulSoup


def knock(website_link):
    i = 0
    news = []
    articles_sorted = []
    success_message_titles = []
    r = requests.get(website_link)
    if r.status_code != 200:
        return f"The URL returned {r.status_code}!"
    soup = BeautifulSoup(r.content, "html.parser")
    for articles_unsorted in soup.find_all("span", {"data-test": "article.type"}):
        if articles_unsorted.text.strip() == f"{sought_type}":
            news.append(i)
        i += 1
    for article_index in news:
        articles_sorted.append("https://www.nature.com" + soup.find_all("a", {"class": "c-card__link u-link-inherit"})
        [article_index]["href"])
    for link in articles_sorted:
        r = requests.get(link)
        if r.status_code != 200:
            return f"The news article URL returned {r.status_code}!"
        soup = BeautifulSoup(r.content, "html.parser")
        file_name = soup.find("title").text.strip()
        for c in string.punctuation:
            file_name = file_name.replace(c, "")
        file_name = file_name.replace(" ", "_").replace("’", "")
        success_message_titles.append(file_name)
        file = open(f"{file_name}.txt", "wb")
        file.write(soup.find("div", {"class": "c-article-body main-content"}).text.encode("utf-8"))
        file.close()
    return f"Saved articles on page {z + 1}:\n{success_message_titles}"


sought_page = int(input())
sought_type = input()
owd = os.getcwd()
for z in range(sought_page):
    os.mkdir(f"Page_{z + 1}")
    os.chdir(f"Page_{z + 1}")
    print(knock(f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={z + 1}"))
    os.chdir(f"{owd}")
print("Articles saved from all pages!")
