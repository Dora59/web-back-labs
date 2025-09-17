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
            'Content-Type': 'text/plai; charset=utf-8'
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
    css_url = url_for("static", filename = "lab1.css")
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
'''  

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
    return "Нет такой страницы", 404 

