from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2 
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))


#функции подключения к БД и отключения
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'darya_pyatina_knowledge_base',
            user = 'darya_pyatina_knowledge_base',
            password = '777',
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name', '')  

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля!')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);", 
                    (login, password_hash, real_name))
    else:
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", 
                    (login, password_hash, real_name))
    
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    #проверим, что пользователь ввел логин и пароль 
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error="Заполните поля!")

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()

    if not user:
        db_close(conn,cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn,cur)
        return render_template('lab5/login.html', 
                               error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn,cur)
    return render_template('/lab5/success_login.html', login=login)


@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    # Простая валидация
    if not title.strip() or not article_text.strip():
        return render_template('lab5/create_article.html', error="Заполните все поля!")

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    login_id = cur.fetchone() ["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (login_id, title, article_text) VALUES (%s, %s, %s);", 
                    (login_id, title, article_text))
    else:
        cur.execute("INSERT INTO articles (login_id, title, article_text) VALUES (?, ?, ?);", 
                    (login_id, title, article_text))
    
    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    login_id = user["id"]

    # Сортируем: сначала избранные, потом остальные
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE login_id=%s ORDER BY is_favorite DESC, id DESC;", (login_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE login_id=? ORDER BY is_favorite DESC, id DESC;", (login_id,))

    articles = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/articles.html', articles=articles)


#Выход из системы
@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
        article = cur.fetchone()
        db_close(conn, cur)
        
        if not article:
            return "Статья не найдена"
            
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", 
                    (title, article_text, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", 
                    (title, article_text, article_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))
        
    db_close(conn, cur)
    return redirect('/lab5/list')

#доп.задание 
#Страница всех пользователей
@lab5.route('/lab5/users')
def all_users():
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    
    users = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/all_users.html', users=users)


#смена имени и пароля
@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT real_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT real_name FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        current_name = user['real_name'] if user and user['real_name'] else ""
        db_close(conn, cur)
        
        return render_template('lab5/profile.html', current_name=current_name)

    # Обработка формы
    real_name = request.form.get('real_name')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Получаем текущего пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    
    # Проверка текущего пароля если меняется пароль
    if new_password:
        if not current_password:
            db_close(conn, cur)
            return render_template('lab5/profile.html', current_name=real_name, error="Введите текущий пароль")
        
        if not check_password_hash(user['password'], current_password):
            db_close(conn, cur)
            return render_template('lab5/profile.html', current_name=real_name, error="Неверный текущий пароль")
        
        if new_password != confirm_password:
            db_close(conn, cur)
            return render_template('lab5/profile.html', current_name=real_name, error="Пароли не совпадают")
        
        # Обновляем пароль
        new_password_hash = generate_password_hash(new_password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET password=%s, real_name=%s WHERE login=%s;", 
                        (new_password_hash, real_name, login))
        else:
            cur.execute("UPDATE users SET password=?, real_name=? WHERE login=?;", 
                        (new_password_hash, real_name, login))
    else:
        # Обновляем только имя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s WHERE login=%s;", (real_name, login))
        else:
            cur.execute("UPDATE users SET real_name=? WHERE login=?;", (real_name, login))
    
    db_close(conn, cur)
    return redirect('/lab5/profile')


