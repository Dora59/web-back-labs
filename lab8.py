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
            login_user(user, remember = False)
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
    return redirect('/lab8/')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "Список статей"


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/create')
def create():
    return "Создание статьи"
