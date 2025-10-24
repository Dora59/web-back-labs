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