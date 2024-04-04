from webapp.news.models import News
from flask import Blueprint, current_app, render_template
from webapp.weather import weather_by_city

blueprint = Blueprint('news', __name__, url_prefix='/news')

@blueprint.route('/')
def index():
    title = "Новости Python"
    # html = get_html("https://www.python.org/blogs/")
    weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    # news_list = get_python_news(html)
    news_list = News.query.order_by(News.published.desc()).all()
    return render_template('news/index.html', page_title=title, weather=weather, news_list=news_list)