from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user
lab8 = Blueprint('lab8', __name__)
 

@lab8.route('/lab8/')
def index():
    # Проверяем авторизацию через Flask-Login
    if current_user.is_authenticated:
        login = current_user.login
    else:
        login = None

    return render_template('lab8/lab8.html', login=login)


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    print(f"Метод запроса: {request.method}")  # Отладка
    if request.method == 'GET':
        print("GET запрос - отдаю пустую форму")
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember') == 'true'
    
    print(f"Получены данные: логин='{login_form}', пароль='{password_form}'")  # Отладка

    # Проверка логина на пустоту
    if not login_form or login_form.strip() == '':
        print("ОШИБКА: логин пустой")
        return render_template('lab8/login.html',
                               error='Логин не может быть пустым')
    
    # Проверка пароля на пустоту
    if not password_form or password_form.strip() == '':
        print("ОШИБКА: пароль пустой")
        return render_template('lab8/login.html',
                               error='Пароль не может быть пустым')

    user = users.query.filter_by(login=login_form).first()
    
    # Проверка пользователя и пароля 
    if user:
        if check_password_hash(user.password, password_form):
            #передаём remember=remember_me
            login_user(user, remember=remember_me)
            return redirect('/lab8/')
    
    return render_template('lab8/login.html',
                           error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка: имя пользователя не должно быть пустым
    if not login_form or login_form.strip() == '':
        return render_template('lab8/register.html',
                               error = 'Имя пользователя не может быть пустым')
    
    # Проверка: пароль не должен быть пустым
    if not password_form or password_form.strip() == '':
        return render_template('lab8/register.html',
                               error = 'Пароль не может быть пустым')

    #поиск пользователя
    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                           error = 'Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    
    return redirect('/lab8/')


@lab8.route('/lab8/articles/')
def article_list():
    search_query = request.args.get('q', '').strip()
    
    # Базовый запрос
    if current_user.is_authenticated:
        # Авторизованные: публичные + свои
        query = articles.query.filter(
            (articles.is_public == True) | (articles.login_id == current_user.id)
        )
    else:
        # Неавторизованные: только публичные
        query = articles.query.filter_by(is_public=True)
    
    # Если есть поисковый запрос
    if search_query:
        # Регистронезависимый поиск по заголовку ИЛИ тексту
        search_filter = db.or_(
            articles.title.ilike(f'%{search_query}%'),
            articles.article_text.ilike(f'%{search_query}%')
        )
        query = query.filter(search_filter)
    
    # Получаем результаты
    articles_list = query.order_by(articles.id.desc()).all()
    
    return render_template('lab8/articles.html', 
                          articles=articles_list,
                          search_query=search_query)


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create', methods=['GET', 'POST'])
def create():
    if not current_user.is_authenticated:
        return redirect('/lab8/login')
    
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'true'  # Проверяем чекбокс
    
    if not title or title.strip() == '':
        return render_template('lab8/create.html',
                               error='Заголовок не может быть пустым')
    
    if not article_text or article_text.strip() == '':
        return render_template('lab8/create.html',
                               error='Текст статьи не может быть пустым')
    
    # Создаем статью в БД
    new_article = articles(
        title=title,
        article_text=article_text,
        login_id=current_user.id,
        is_public=is_public,  
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles')


@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        return "У вас нет прав на редактирование", 403
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'true'
    
    if not title or title.strip() == '':
        return render_template('lab8/edit.html', 
                               article=article,
                               error='Заголовок не может быть пустым')
    
    if not article_text or article_text.strip() == '':
        return render_template('lab8/edit.html', 
                               article=article,
                               error='Текст статьи не может быть пустым')
    
    # Обновляем статью
    article.title = title
    article.article_text = article_text
    article.is_public = is_public  # Обновляем статус публичности
    
    db.session.commit()
    
    return redirect('/lab8/articles')


@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    # Находим статью
    article = articles.query.get_or_404(article_id)
    
    # Проверяем, что пользователь - автор статьи
    if article.login_id != current_user.id:
        return "У вас нет прав на удаление этой статьи", 403
    
    # Удаляем статью
    db.session.delete(article)
    db.session.commit()
    
    return redirect('/lab8/articles')