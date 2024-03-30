from flask import Flask, render_template, flash, redirect, url_for
from webapp.forms import LoginForm
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from webapp.model import db, News, User
from webapp.weather import weather_by_city




# from jinja2 import Template, FileSystemLoader, Environment

# # Configure the template directory
# env = Environment(loader=FileSystemLoader('template'))

# # Render a template that doesn't exist
# template = env.get_template('login.html')


def create_app():
    # app = Flask(__name__)
    app = Flask(__name__, template_folder='template')
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    @app.route('/')
    def index():
        title = "Новости Python"
        # html = get_html("https://www.python.org/blogs/")
        weather = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        # news_list = get_python_news(html)
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)
    

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)
    
    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))
    

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ'
        else:
            return 'Ты не админ!'

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))


    return app

# if __name__=="__main__":
#     app.run(debug=True)