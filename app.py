from flask import Flask, url_for, request, redirect
import datetime 
app = Flask(__name__)

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
            </ul>
        </div>

        <footer>
            <hr>
            <p>Пятина Дарья Вадимовна, ФБИ-31, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''  
@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная работа 1</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, 
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится 
        к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, 
        сознательно предоставляющих лишь самые базовые возможности.</p>

        <a href="/">На главную</a>

        <h2>Список роутов</h2>
        <ul>
            <li><a href="/">Главная страница</a></li>
            <li><a href="/index">Index (дублирует главную)</a></li>
            <li><a href="/lab1">Лабораторная работа 1</a></li>
            <li><a href="/lab1/web">Web-сервер на Flask</a></li>
            <li><a href="/lab1/author">Информация об авторе</a></li>
            <li><a href="/lab1/image">Изображение дуба</a></li>
            <li><a href="/lab1/counter">Счетчик посещений</a></li>
            <li><a href="/lab1/counter/clear">Очистка счетчика</a></li>
            <li><a href="/lab1/info">Редирект на автора</a></li>
            <li><a href="/lab1/created">Создано успешно (201)</a></li>
            <li><a href="/bad_request">400 Bad Request</a></li>
            <li><a href="/unauthorized">401 Unauthorized</a></li>
            <li><a href="/payment_required">402 Payment Required</a></li>
            <li><a href="/forbidden">403 Forbidden</a></li>
            <li><a href="/method_not_allowed">405 Method Not Allowed</a></li>
            <li><a href="/teapot">418 I'm a teapot</a></li>
            <li><a href="/server_error">500 Internal Server Error</a></li>
        </ul>
    </body>
</html>'''


@app.route("/lab1/web")
def web():
    return '''<!doctype html>
        <html>
           <body> 
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
               <a href="/lab1/image">oak</a>
           </body> 
        </html>''', 200, {
            "X-Server": "sample",
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():  
    name = "Пятина Дарья Вадимовна"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/image')
def image():
    path = url_for("static", filename="oak.jpeg")
    css_url = url_for("static", filename="lab1.css")
    
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_url + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <a href="/lab1/web">web</a>
        <img src="''' + path + '''">
    </body>
</html>
''', 200, {
    'Content-Language': 'ru-RU',  
    'X-Developer-Name': 'Пятина Дарья Вадимовна',
    'X-Student-Group': 'ФБИ-31', 
    'X-Custom-Header': 'Лабораторная работа по веб-программированию',
    'X-University': 'НГТУ',  
    'X-Academic-Year': '2024-2025'  
}

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы посещали данную страницу: ''' + str (count) + '''
        <hr>
        <a href="/lab1/counter/clear">Очистить счетчик</a>
        <hr>
        Дата и время: ''' + str (time) + ''' <br>
        Запрошенный адрес: ''' + str (url) + ''' <br>
        Ваш IP-адрес: ''' + str (client_ip) + ''' <br>
    </body>
</html>
'''  
@app.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')


@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
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
    css_url = url_for("static", filename="lab1.css")
    image_url = url_for("static", filename="404.jpg")
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

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'