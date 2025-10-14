from flask import Blueprint, url_for, redirect, request
import datetime 
lab1= Blueprint('lab1',__name__)

@lab1.route("/lab1")
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


@lab1.route("/lab1/web")
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

@lab1.route("/lab1/author")
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

@lab1.route('/lab1/image')
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

@lab1.route('/lab1/counter')
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
@lab1.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/lab1/created")
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

