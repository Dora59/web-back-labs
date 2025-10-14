from flask import Flask, url_for, request, redirect, abort, render_template
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
                <li><a href="/lab2/">2 лабораторная работа</a></li>
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

flower_list = [
    {'name': 'Роза', 'price': 300}, 
    {'name': 'Тюльпан', 'price': 250}, 
    {'name': 'Незабудка', 'price': 200}, 
    {'name': 'Ромашка', 'price': 150}
    ]

@app.route('/lab2/flowers/')
def all_flowers():
    return render_template('flower.html', flowers=flower_list)

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
       abort(404)
    else:
        flower = flower_list[flower_id]
        return f"""
        <h2>Цветок: {flower['name']}</h2>
        <p>Цена: {flower['price']} руб</p>
        <a href="/lab2/flowers/">Список всех цветов</a>
    """

@app.route('/lab2/add_flower/', methods=['GET', 'POST'])
@app.route('/lab2/add_flower/<name>')
def add_flower(name=None):
    if name is None:
        if request.method == 'POST':
            name = request.form.get('name')
            if name:
                flower_list.append({'name': name, 'price': 300})
                return redirect('/lab2/flowers/')
            else:
                abort(400, "Вы не задали имя цветка")
        else:
            abort(400, "Вы не задали имя цветка")
    else:
        flower_list.append({'name': name, 'price': 300})
        return redirect('/lab2/flowers/')

@app.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/flowers/')

@app.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers/')

@app.route('/lab2/example')
def example():
    name, lab_num, number, group, course = 'Дарья Пятина', 2, 2, 'ФБИ-31', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html',
                           name=name, lab_num=lab_num, number=number,
                           group=group, course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrases = "<b>Нам</b> <u>дворцов</u> <i>заманчивые</i> своды..."
    return render_template('filter.html', phrases = phrases)


#Пересылка с /lab2/calc/ на /lab2/calc/1/1
@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

# Пересылка с /lab2/calc/<int:a> на /lab2/calc/<int:a>/1
@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('calc', a=a, b=1))

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    # Выполняем математические операции
    sum_result = a + b
    sub_result = a - b
    mul_result = a * b
    
    # Обрабатываем деление с проверкой на ноль
    if b != 0:
        div_result = a / b
        div_display = f'{a} / {b} = {div_result}'
    else:
        div_display = f'{a} / {b} = ошибка (деление на ноль)'
    
    pow_result = a ** b
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>Калькулятор</title>
    </head>
    <body>
        <h2>Расчёт с параметрами:</h2>
        <p>{a} + {b} = {sum_result}</p>
        <p>{a} - {b} = {sub_result}</p>
        <p>{a} × {b} = {mul_result}</p>
        <p>{div_display}</p>
        <p>{a}^{b} = {pow_result}</p>
    </body>
</html>
'''


books = [
    {
        'author': 'Николай Карамзин',
        'title': 'Бедная Лиза',
        'genre': 'Сентиментальная повесть',
        'pages': '224'
    },
    {
        'author': 'Александр Грибоедов',
        'title': 'Горе от ума',
        'genre': 'Комедия',
        'pages': '160'
    },
    {
        'author': 'Александр Пушкин',
        'title': 'Евгений Онегин',
        'genre': 'Роман в стихах',
        'pages': '224'
    },
    {
        'author': 'Михаил Лермонтов',
        'title': 'Герой нашего времени',
        'genre': 'Психологический роман',
        'pages': '256'
    },
    {
        'author': 'Николай Гоголь',
        'title': 'Миргород',
        'genre': 'Цикл повестей',
        'pages': '368'
    },
    {
        'author': 'Николай Лесков',
        'title': 'Левша',
        'genre': 'Художественная литература',
        'pages': '224'
    },
    {
        'author': 'Михаил Салтыков-Щедрин',
        'title': 'История одного города',
        'genre': 'Сатирическая повесть',
        'pages': '288'
    },
    {
        'author': 'Иван Бунин',
        'title': 'Митина любовь',
        'genre': 'Проза',
        'pages': '448'
    },
    {
        'author': 'Юрий Олеша',
        'title': 'Три Толстяка',
        'genre': 'Проза',
        'pages': '208'
    },
    {
        'author': 'Михаил Булгаков',
        'title': 'Мастер и Маргарита',
        'genre': 'Проза',
        'pages': '480'
    }
]

@app.route('/lab2/books/')
def show_books():
    return render_template('books.html', books=books)


cities = [
    {
        'name': 'Москва',
        'image': 'city1.jpg',
        'description': 'Первый по размерам город РФ.'
    },

    {
        'name': 'Краснодар',
        'image': 'city2.jpg',
        'description': 'Краснодар — южная столица РФ.'
    },

    {
        'name': 'Калининград',
        'image': 'city3.jpeg',
        'description': 'Самый западный город РФ.'
    },

    {
        'name': 'Санкт-Петербург',
        'image': 'city4.jpg',
        'description': 'Величественный, очаровательный, мистический Питер давно стал меккой творческих людей.'
    },

    {
        'name': 'Тюмень',
        'image': 'city5.jpg',
        'description': 'С 2015 года Тюмень занимает лидирующие позиции в рейтингах качества дорожного полотна.'
    },

    {
        'name': 'Сочи',
        'image': 'city6.jpg',
        'description': 'Город-мечта для многих жителей северных регионов.'
    },

    {
        'name': 'Нижний Новгород',
        'image': 'city7.jpg',
        'description': 'Город, который целиком входит во Всемирное наследие ЮНЕСКО. '
    },

    {
        'name': 'Казань',
        'image': 'city8.jpeg',
        'description': 'Жемчужина среди российских центров туризма'
    },

    {
        'name': 'Екатеринбург',
        'image': 'city9.jpg',
        'description': 'Зима в Екатеринбурге снежная, морозная и долгая, лето редко бывает жарким.'
    },

    {
        'name': 'Новосибирск',
        'image': 'city10.jpg',
        'description': 'Новосибирск — третий по численности населения город России и крупнейший мегаполис Сибири.'
    },

    {
        'name': 'Калуга',
        'image': 'city11.jpg',
        'description': 'Здесь ярко выражены все 4 времени года, и можно насладиться преимуществами каждого из них.'
    },

    {
        'name': 'Набережные Челны',
        'image': 'city12.jpg',
        'description': 'Город в Татарстане на берегу реки Кама.'
    },

    {
        'name': 'Уфа',
        'image': 'city13.jpg',
        'description': 'Столица Башкирии'
    },

    {
        'name': 'Севастополь',
        'image': 'city14.jpg',
        'description': ' Расположение на Чёрном море делает город привлекательным для летнего отдыха'
    },

    {
        'name': 'Грозный',
        'image': 'city15.jpg',
        'description': 'Чтобы жить в Грозном, важно уважать местные традиции и культуру.'
    },

    {
        'name': 'Мурманск',
        'image': 'city16.jpg',
        'description': 'Восемь месяцев в году здесь можно любоваться северным сиянием.'
    },

    {
        'name': 'Владивосток',
        'image': 'city17.jpg',
        'description': 'Владивосток — портовый город на берегу Японского моря'
    },

    {
        'name': 'Пермь',
        'image': 'city18.jpg',
        'description': 'Пермь — крупный промышленный и культурный центр на Урале'
    },

    {
        'name': 'Иркутск',
        'image': 'city19.jpg',
        'description': 'Иркутск — исторический город в Восточной Сибири'
    },

    {
        'name': 'Томск',
        'image': 'city20.jpg',
        'description': 'Томск — старейший научный и образовательный центр Сибири'
    }
]

@app.route('/lab2/cities/')
def show_cities():
    html = '<h1>Города России</h1>'

    for city in cities:
        html += f'''
        <div style = "border: 4px solid purple; padding: 10px; margin: 10px; width: 350px;">
            <h2>{ city [ "name" ]}</h2>
            <img src="/static/{ city [ 'image' ]}" width="350">
            <p>{ city ["description" ]}</p>
        </div>
        '''
    return html 
