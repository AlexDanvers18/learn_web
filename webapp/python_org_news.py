from datetime import datetime
from webapp.model import db, News
import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False
    
def get_python_news(html):
    html = get_html("https://www.python.org/blogs/")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            try:
                published = datetime.strptime(published, '%Y-%m-%d')
            except(ValueError):
                published = datetime.now()
            save_news(title=title, url=url, published=published)
        #     result_news.append({
        #         "title": title,
        #         "url": url,
        #         "published": published
        #     })
        # return result_news
    return False
    

def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()

# def get_python_news(html):
#     html = get_html("https://www.python.org/blogs/")
#     soup = BeautifulSoup(html, 'html.parser')
#     all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
#     result_news = []
#     for news in all_news:
#         title = news.find('a').text
#         url = news.find('a')['href']
#         published = news.find('time').text
#         result_news.append({
#             "title": title,
#             "url": url,
#             "published": published
#         })
#     return result_news


if __name__ == "__main__":
    html = get_html("https://www.python.org/blogs/")
    if html:
        get_python_news(html)