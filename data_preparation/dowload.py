import os
from bs4 import BeautifulSoup
import requests


def download_story(title: str, story_url: str, author_dir: str):
    os.makedirs(author_dir, exist_ok=True)
    story_page = requests.get(story_url)
    current_story_file = (author_dir + "/" + title + ".txt").replace("?", "").replace("\"", "")
    if not os.path.exists(current_story_file):
        with open(current_story_file, "w+", encoding="UTF-8") as file:
            story_soup = BeautifulSoup(story_page.content)
            paragraphs = story_soup.select("#mw-content-text > div.mw-parser-output > div.indent > p")
            paragraphs_text = [p.text for p in paragraphs]
            print(paragraphs_text)
            file.writelines(paragraphs_text)
            file.flush()


def remove_empty_files(dir: str):
    for fileName in os.listdir(dir):
        file_path = dir + os.path.sep + fileName
        if os.path.getsize(file_path) == 0:
            os.remove(file_path)
            print(file_path + " removed, because it's empty.")


def get_soup(url: str):
    author_page = requests.get(url)
    soup = BeautifulSoup(author_page.content)
    return soup


def download_chekhov():
    url = "https://ru.wikisource.org/wiki/%D0%90%D0%BD%D1%82%D0%BE%D0%BD_%D0%9F%D0%B0%D0%B2%D0%BB%D0%BE%D0%B2%D0%B8" \
          "%D1%87_%D0%A7%D0%B5%D1%85%D0%BE%D0%B2 "
    soup = get_soup(url)
    stories_list = soup.select("#mw-content-text > div > ul:nth-child(21) > li > a")
    base_wiki_source_url = "https://ru.wikisource.org"
    chekhov_dir = "../data/A_P_Chehov"
    for link in stories_list:
        download_story(link["title"], base_wiki_source_url + link["href"], chekhov_dir)
    remove_empty_files(chekhov_dir)


def download_kuprin():
    url = "https://ru.wikisource.org/wiki/%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80_%D0%98%D0%B2%D0%B0" \
          "%D0%BD%D0%BE%D0%B2%D0%B8%D1%87_%D0%9A%D1%83%D0%BF%D1%80%D0%B8%D0%BD "
    soup = get_soup(url)
    stories_list = soup.select("#mw-content-text > div > ul:nth-child(16) > li > a:not(.new)")
    stories_list2 = soup.select("#mw-content-text > div > ul:nth-child(18) > li > a:not(.new)")
    stories_list = stories_list + stories_list2

    base_wiki_source_url = "https://ru.wikisource.org"
    kuprin_dir = "../data/A_I_Kuprin"
    for link in stories_list:
        download_story(link["title"], base_wiki_source_url + link["href"], kuprin_dir)
    remove_empty_files(kuprin_dir)


# download_chekhov()
download_kuprin()