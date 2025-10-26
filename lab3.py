from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')

    if name is None:
        name = "Аноним"
    
    if age is None:
        age = "Не указан"
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Darya', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'blue')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors={}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Вы не заполнили поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    #Напишем стоимость каждого напитка 
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    #Добавка молока удорожает напиток на 30 рублей, а сахара - на 10
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success', methods=['POST'])
def success():
    price = request.form.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    background = request.args.get('background')
    font_size = request.args.get('font_size')

    if color or background or font_size:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if background:
            resp.set_cookie('background', background)
        if font_size:
            resp.set_cookie('font_size', font_size)
        return resp

    color = request.cookies.get('color')
    background = request.cookies.get('background')
    font_size = request.cookies.get('font_size')
    resp = make_response(render_template('lab3/settings.html', color=color, background=background, font_size=font_size))
    return resp

@lab3.route('/lab3/settings/reset')
def reset_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('background')
    resp.delete_cookie('font_size')
    return resp


@lab3.route('/lab3/ticket')
def ticket():
    return render_template('lab3/ticket_form.html')


@lab3.route('/lab3/ticket_result', methods=['POST'])
def ticket_result():
    # получение данных из форм 
    fio = request.form.get('fio')
    shelf = request.form.get('shelf')
    linen = request.form.get('linen')
    baggage = request.form.get('baggage')
    age = request.form.get('age')
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    date = request.form.get('date')
    insurance = request.form.get('insurance')

    # проверка на пустые поля
    errors = {}
    if not fio:
        errors['fio'] = 'Заполните ФИО пассажира'
    if not shelf:
        errors['shelf'] = 'Выберите тип полки'
    if not age:
        errors['age'] = 'Заполните возраст'
    elif not age.isdigit() or int(age) < 1 or int(age) > 120:
        errors['age'] = 'Возраст должен быть от 1 до 120 лет'
    if not departure:
        errors['departure'] = 'Заполните пункт выезда'
    if not destination:
        errors['destination'] = 'Заполните пункт назначения'
    if not date:
        errors['date'] = 'Выберите дату поездки'

    # Если есть ошибки, показываем форму снова
    if errors:
        return render_template('lab3/ticket_form.html', errors=errors, 
                              fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                              age=age, departure=departure, destination=destination,
                              date=date, insurance=insurance)
    
    # Расчет стоимости билета
    age_int = int(age)
    if age_int < 18:
        base_price = 700  
        ticket_type = "Детский билет"
    else:
        base_price = 1000 
        ticket_type = "Взрослый билет"

    # Доплаты
    additional_cost = 0
    if shelf in ['lower', 'lower-side']:
        additional_cost += 100
    if linen == 'on':
        additional_cost += 75
    if baggage == 'on':
        additional_cost += 250
    if insurance == 'on':
        additional_cost += 150

    total_price = base_price + additional_cost

    return render_template('lab3/ticket_result.html', 
                          fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                          age=age, departure=departure, destination=destination,
                          date=date, insurance=insurance,
                          ticket_type=ticket_type, total_price=total_price)


#доп.задание
#Список автомобилей Mercedes 
cars = [
    {'name': 'Mercedes A-Class', 'price': 2500000, 'year': 2023, 'color': 'белый'},
    {'name': 'Mercedes C-Class', 'price': 3500000, 'year': 2023, 'color': 'черный'},
    {'name': 'Mercedes E-Class', 'price': 4500000, 'year': 2023, 'color': 'серый'},
    {'name': 'Mercedes S-Class', 'price': 8000000, 'year': 2023, 'color': 'синий'},
    {'name': 'Mercedes GLA', 'price': 2800000, 'year': 2023, 'color': 'красный'},
    {'name': 'Mercedes GLC', 'price': 4200000, 'year': 2023, 'color': 'зеленый'},
    {'name': 'Mercedes GLE', 'price': 5500000, 'year': 2023, 'color': 'коричневый'},
    {'name': 'Mercedes GLS', 'price': 7500000, 'year': 2023, 'color': 'бежевый'},
    {'name': 'Mercedes CLS', 'price': 5000000, 'year': 2023, 'color': 'фиолетовый'},
    {'name': 'Mercedes AMG GT', 'price': 12000000, 'year': 2023, 'color': 'желтый'},
    {'name': 'Mercedes G-Class', 'price': 15000000, 'year': 2023, 'color': 'черный'},
    {'name': 'Mercedes B-Class', 'price': 2300000, 'year': 2023, 'color': 'оранжевый'},
    {'name': 'Mercedes V-Class', 'price': 4800000, 'year': 2023, 'color': 'серебристый'},
    {'name': 'Mercedes SL', 'price': 6800000, 'year': 2023, 'color': 'голубой'},
    {'name': 'Mercedes CLA', 'price': 3200000, 'year': 2023, 'color': 'бордовый'},
    {'name': 'Mercedes GLB', 'price': 3100000, 'year': 2023, 'color': 'бирюзовый'},
    {'name': 'Mercedes EQE', 'price': 5200000, 'year': 2023, 'color': 'синий'},
    {'name': 'Mercedes EQS', 'price': 9000000, 'year': 2023, 'color': 'черный'},
    {'name': 'Mercedes AMG C63', 'price': 6500000, 'year': 2023, 'color': 'красный'},
    {'name': 'Mercedes AMG E53', 'price': 5800000, 'year': 2023, 'color': 'серый'}
]

@lab3.route('/lab3/cars')
def cars_search():
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    if min_price is None:
        min_price = request.cookies.get('min_price', '')
    if max_price is None:
        max_price = request.cookies.get('max_price', '')

    if request.args.get('reset'):
        min_price = ''
        max_price = ''

    all_prices = [car['price'] for car in cars]
    min_all = min(all_prices)
    max_all = max(all_prices)

    filtered_cars = []

    for car in cars:
        price = car['price']
        include = True

        if min_price and price < float(min_price):
            include = False 

        if max_price and price > float(max_price):
            include = False 

        if min_price and max_price and float(min_price) > float(max_price):
            #Если пользователь перепутал цены, меняем условие
            if float(max_price) <= price <= float(min_price):
                include = True
            else:
                include = False

        #Добавляем автомобиль в результат, если он прошел все проверки
        if include:
            filtered_cars.append(car)

    if not min_price and not max_price:
            filtered_cars = cars      

    resp = make_response(render_template('lab3/cars.html',
                                        cars=filtered_cars,
                                        min_price=min_price,
                                        max_price=max_price,
                                        min_all=min_all,
                                        max_all=max_all,
                                        count=len(filtered_cars)))
    
    
    #Работа с куки
    if request.args.get('reset'):
            #Удаляем куки при нажатии "Сброс"
            resp.delete_cookie('min_price')
            resp.delete_cookie('max_price')
    else:
            #Сохраняем значения в куки при поиске
        if min_price:
                resp.set_cookie('min_price', min_price)
        if max_price:
                resp.set_cookie('max_price', max_price)
        
    #Возврат готового ответа
    return resp       