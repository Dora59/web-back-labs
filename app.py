import os
from flask import Flask, url_for, request, redirect, abort, render_template
from lab1 import lab1
from lab2 import lab2 as lab2_blueprint 
from lab3 import lab3 
from lab4 import lab4
from lab5 import lab5
import datetime 

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1) 
app.register_blueprint(lab2_blueprint) 
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)


@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title> 
    </head>
    <body>
         <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>

        <div>
            <ul>
                <li><a href="/lab1">1 лабораторная Работа</a></li>
                <li><a href="/lab2/">2 лабораторная работа</a></li>
                <li><a href="/lab3/">3 лабораторная работа</a></li>
                <li><a href="/lab4/">4 лабораторная работа</a></li>
                <li><a href="/lab5/">5 лабораторная работа</a></li>
                <li><a href="/lab6/">6 лабораторная работа</a></li>
            </ul>
        </div>

        <footer>
            <hr>
            <p>Пятина Дарья Вадимовна, ФБИ-31, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''  

    return '''  
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>Что-то создано...</i></div>
    </body>
</html>   
''', 201

@app.errorhandler(404)
def not_found(err):
    css_url = url_for("static", filename="lab1/lab1.css")
    image_url = url_for("static", filename="lab1/404.jpg")
    return '''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <link rel="stylesheet" href="''' + css_url + '''">
    </head>
    <body>
        <div style="text-align: center; padding: 50px;">
            <h1 style="color: #e74c3c; font-size: 48px;">404</h1>
            <h2>Ой! Страница потерялась</h2>
            
            <img src="''' + image_url+ '''">  
            
            <p>К сожалению, страница которую вы ищете, не существует.</p>
            <p>Возможно, она была перемещена или удалена.</p>
            
            <div>
                <a href="/">На главную</a>
            </div>
        </div>
    </body>
</html>
''', 404

# Коды ответов HTTP
@app.route('/bad_request')
def bad_request():
    return '''
<!doctype html>
<html>
    <head>
        <title>400 Bad Request</title>
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может обработать запрос из-за неверного синтаксиса.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 400

@app.route('/unauthorized')
def unauthorized():
    return '''
<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 401

@app.route('/payment_required')
def payment_required():
    return '''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Запрос не может быть обработан до осуществления оплаты.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 402

@app.route('/forbidden')
def forbidden():
    return '''
<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ к запрашиваемому ресурсу запрещен.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 403

@app.route('/method_not_allowed')
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод запроса известен серверу, но не поддерживается для целевого ресурса.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 405

@app.route('/teapot')
def teapot():
    return '''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я чайник!</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 418

# Обработчик, который вызывает ошибку сервера (500)
@app.route('/server_error')
def server_error():
    result = 10 / 0
    return 

# Перехватчик ошибки 500 
@app.errorhandler(500)
def internal_server_error(err):
    css_url = url_for("static", filename="lab1.css")
    
    return '''
<!doctype html>
<html>
    <head>
        <title>500 - Ошибка сервера</title>
        <link rel="stylesheet" href="''' + css_url + '''">
    </head>
    <body class="error-page">
        <h1 class="error-code">500</h1>
        <h2 class="error-title">Внутренняя ошибка сервера</h2>
        
        <div style="background: white; color: #333; padding: 20px; border-radius: 10px; max-width: 600px; margin: 20px;">
            <h3>Что случилось?</h3>
            <p>На сервере произошла непредвиденная ошибка. Мы уже работаем над исправлением.</p>
            
            <h3>Что можно сделать?</h3>
            <ul>
                <li>Попробуйте обновить страницу</li>
                <li>Вернитесь на главную страницу</li>
                <li>Если ошибка повторяется, сообщите администратору</li>
            </ul>
        </div>
        
        <div class="error-buttons">
            <a href="/" class="error-button">На главную</a>
        </div>
        
        <div style="margin-top: 30px; color: rgba(255,255,255,0.8);">
            <p>Пятина Дарья Вадимовна, ФБИ-31</p>
        </div>
    </body>
</html>
''', 500

