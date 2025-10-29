from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('/lab4/div.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)

    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)



# Суммирование
@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

# Умножение 
@lab4.route('/lab4/multiply-form')
def multiply_form():
    return render_template('lab4/multiply-form.html')

@lab4.route('/lab4/multiply', methods=['POST'])
def multiply():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    # Если поле пустое, считаем как 1
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    
    result = x1 * x2
    return render_template('lab4/multiply.html', x1=x1, x2=x2, result=result)

# Вычитание
@lab4.route('/lab4/subtract-form')
def subtract_form():
    return render_template('lab4/subtract-form.html')

@lab4.route('/lab4/subtract', methods=['POST'])
def subtract():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/subtract.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/subtract.html', x1=x1, x2=x2, result=result)

# Возведение в степень
@lab4.route('/lab4/power-form')
def power_form():
    return render_template('lab4/power-form.html')

@lab4.route('/lab4/power', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/power.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/power.html', error='Оба числа не могут быть равны нулю!')
    
    result = x1 ** x2
    return render_template('lab4/power.html', x1=x1, x2=x2, result=result)


tree_count = 0
max_trees = 5

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, max_trees=max_trees)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:  
        tree_count -= 1
    elif operation == 'plant' and tree_count < max_trees: 
        tree_count += 1
    
    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Попов', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Смит', 'gender': 'male'},
    {'login': 'dora', 'password': '333', 'name': 'Дора Сидорова', 'gender': 'female'},
    {'login': 'den', 'password': '444', 'name': 'Денис Мельков', 'gender': 'male'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized=True
            #находим пользователя для получения информации
            user = next((u for u in users if u['login'] == session['login']), None)
            name = user['name'] if user else session['login']
            return render_template("lab4/login.html", authorized=authorized, name=name)
        else:
            return render_template("lab4/login.html", authorized=False)
    
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые значения
    errors = []
    if not login:
        errors.append('Не введён логин')
    if not password:
        errors.append('Не введён пароль')
    
    if errors:
        return render_template('/lab4/login.html', errors=errors, login_value=login, authorized=False)
    
    # Проверка логина и пароля
    user = next((u for u in users if u['login'] == login and u['password'] == password), None)
    
    if user:
        session['login'] = login
        return redirect('/lab4/login')

    error = 'Неверные логини и/или пароль'
    return render_template('/lab4/login.html', error=error, authorized=False)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


#ХОЛОДИЛЬНИК 
@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    # Получаем температуру из формы
    temperature = request.form.get('temperature')
    
    # Проверяем, задана ли температура
    if not temperature:
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    #Преобразуем в число
    try:
        temp = int(temperature)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: введите число')
    
    #диапазоны температуры
    if temp < -12:
        return render_template('lab4/fridge.html', error='Слишком низкое значение')
    elif temp > -1:
        return render_template('lab4/fridge.html', error='Слишком высокое значение')
    elif -12 <= temp <= -9:
        snowflakes = 3
        message = f'Установлена температура: {temp}°C'
    elif -8 <= temp <= -5:
        snowflakes = 2
        message = f'Установлена температура: {temp}°C'
    elif -4 <= temp <= -1:
        snowflakes = 1
        message = f'Установлена температура: {temp}°C'
    else:
        snowflakes = 0
        message = f'Установлена температура: {temp}°C'
    
    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes, temperature=temp)


#Заказ зерна
@lab4.route('/lab4/grain-order', methods=['GET', 'POST'])
def grain_order():
    # Цены на зерно
    prices = {
        'barley': 12000,  
        'oats': 8500,     
        'wheat': 9000,    
        'rye': 15000     
    }
    
    # Русские названия 
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    if request.method == 'GET':
        return render_template('lab4/grain_order.html')
    
    # Получаем данные из формы
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    # Проверка на пустой вес
    if not weight:
        return render_template('lab4/grain_order.html', error='Ошибка: не указан вес')
    
    try:
        weight = float(weight)
    except ValueError:
        return render_template('lab4/grain_order.html', error='Ошибка: вес должен быть числом')
    
    # Проверка на отрицательный или нулевой вес
    if weight <= 0:
        return render_template('lab4/grain_order.html', error='Ошибка: вес должен быть больше 0')
    
    # Проверка на слишком большой объем
    if weight > 100:
        return render_template('lab4/grain_order.html', error='Извините, такого объёма сейчас нет в наличии')
    
    # Рассчитываем стоимость
    price_per_ton = prices[grain_type]
    total = weight * price_per_ton
    
    #скидка 10% за объем более 10 тонн
    discount = 0
    if weight > 10:
        discount = total * 0.10
        total -= discount
    
    grain_name = grain_names[grain_type]
    
    return render_template('lab4/grain_order.html', 
                         success=True,
                         grain_name=grain_name,
                         weight=weight,
                         total=total,
                         discount=discount,
                         has_discount=weight > 10)