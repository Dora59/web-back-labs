from flask import Blueprint, abort, url_for, redirect, request, render_template
import datetime 
lab2= Blueprint('lab2',__name__, template_folder='templates/lab2')

@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = [
    {'name': 'Роза', 'price': 300}, 
    {'name': 'Тюльпан', 'price': 250}, 
    {'name': 'Незабудка', 'price': 200}, 
    {'name': 'Ромашка', 'price': 150}
    ]

@lab2.route('/lab2/flowers/')
def all_flowers():
    return render_template('lab2/flower.html', flowers=flower_list)


@lab2.route('/lab2/flowers/<int:flower_id>')
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


@lab2.route('/lab2/add_flower/', methods=['GET', 'POST'])
@lab2.route('/lab2/add_flower/<name>')
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


@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/flowers/')


@lab2.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers/')


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrases = "<b>Нам</b> <u>дворцов</u> <i>заманчивые</i> своды..."
    return render_template('filter.html', phrases = phrases)


#Пересылка с /lab2/calc/ на /lab2/calc/1/1
@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1))


# Пересылка с /lab2/calc/<int:a> на /lab2/calc/<int:a>/1
@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('lab2.calc', a=a, b=1))


@lab2.route('/lab2/calc/<int:a>/<int:b>')
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


@lab2.route('/lab2/books/')
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


@lab2.route('/lab2/cities/')
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