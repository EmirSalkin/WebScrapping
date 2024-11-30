# https://www.azquotes.com/ sitesinden authors, topics, quote of the day lerin scrapping edilmesi

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

def scrape_authors():
    authors = []
    url = "https://www.azquotes.com/quotes/authors.html"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    href_values = [
        "https://www.azquotes.com" + a["href"]
        for a in soup.select("ul a.more")
    ]

    for href in tqdm(href_values, desc="Authors scrapping...", ncols=100, colour="red"):
        while href:
            page_response = requests.get(href)
            page_soup = BeautifulSoup(page_response.content, "html.parser")
            for tr in page_soup.select("tbody tr"):
                authors.append(tr.find("a").get_text(strip=True) if tr.find("a") else None)
            
            next_li = page_soup.find("li", class_="next")
            href = "https://www.azquotes.com" + next_li.find("a")["href"] if next_li and next_li.find("a") else None

    with open("authors.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(authors))

def scrape_topics():
    topics = []
    url = "https://www.azquotes.com/quotes/topics/index.html"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    topic_hrefs = [
        "https://www.azquotes.com" + a["href"]
        for a in soup.select("ul a.more")
    ]

    for href in tqdm(topic_hrefs, desc="Topics Scrapping...", ncols=100, colour="blue"):
        page_response = requests.get(href)
        page_soup = BeautifulSoup(page_response.content, "html.parser")
        for a in page_soup.select("section.authors-page ul a"):
            topics.append(a.get_text(strip=True))

    with open("topics.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(topics))

def scrape_quotes():
    quote_text = []
    page = 1

    url = "https://www.azquotes.com/quote_of_the_day.html"
    while True:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        print(page)
        div_tag = soup.find("ul", class_="list-quotes")
        if not div_tag:
            print("Quotes list not found.")
            continue

        div_tags = div_tag.find_all("div", class_ = "wrap-block")
        for tag in div_tags:
            title_link = tag.find("a", class_="title")
            if title_link:
                text = title_link.text.strip()
            else:
                text = None

            author_div = tag.find("div")
            if author_div:
                author = author_div.text.strip()
            else:
                author = None
            metin = author, "-->", text
            quote_text.append(metin)
        # * next page button search
        next_li = soup.find("li", class_="next")
        if next_li and next_li.find('a'):
            next_href = next_li.find('a')['href']
            url = "https://www.azquotes.com/" + next_href
        else:
            break
        page += 1

    with open("./quote_text.txt", "w", encoding="utf-8") as dosya2:
        print(*quote_text, sep="\n", file=dosya2)

if __name__ == "__main__":
    scrape_authors()
    scrape_topics()
    scrape_quotes()