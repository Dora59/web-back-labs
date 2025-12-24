from flask import Blueprint, render_template, session, jsonify, request
import random
from flask_login import current_user, login_required

lab9 = Blueprint('lab9', __name__)

congratulations = [
    "С Новым Годом!",
    "Желаю счастья!",
    "Будь здоровой!",
    "Удачи во всем!",
    "Исполнения желаний!",
    "Мира и добра!",
    "Успехов в учебе!",
    "Любви и тепла!",
    "Хорошего настроения!",
    "Всего самого лучшего!"
]

def init_session():
    if 'positions' not in session:
        positions = []
        # СЕТКА 5x2 (5 столбцов, 2 строки)
        for row in range(2):
            for col in range(5):
                x = 10 + col * 20  # 10%, 30%, 50%, 70%, 90%
                y = 15 + row * 35  # 15%, 50%
                positions.append((x, y))
        session['positions'] = positions
    
    if 'opened' not in session:
        session['opened'] = []
    
    if 'congrats' not in session:
        shuffled = congratulations.copy()
        random.shuffle(shuffled)
        session['congrats'] = shuffled

@lab9.route('/lab9/')
def main():
    init_session()
    
    # Проверяем авторизацию
    is_auth = current_user.is_authenticated
    
    return render_template('lab9/index.html',
                           positions=session['positions'],
                           opened=session['opened'],
                           total=10,
                           is_auth=is_auth)

@lab9.route('/lab9/open', methods=['POST'])
def open_gift():
    data = request.json
    box_index = data.get('box_index')
    
    if 'opened' not in session:
        session['opened'] = []
    
    # Проверяем, не открыта ли уже коробка
    if box_index in session['opened']:
        return jsonify({'error': 'Эта коробка уже открыта'}), 400
    
    # Проверяем лимит (3 коробки)
    if len(session['opened']) >= 3:
        return jsonify({'error': 'Можно открыть только 3 коробки'}), 400
    
    # Добавляем в открытые
    session['opened'].append(box_index)
    session.modified = True  # Важно для Flask session!
    
    # Получаем поздравление и картинку
    congrats = session['congrats'][box_index]
    gift_img = f"подарок{box_index + 1}.png"
    
    return jsonify({
        'success': True,
        'congrats': congrats,
        'gift': gift_img,
        'opened_count': len(session['opened']),
        'remaining': 10 - len(session['opened'])
    })

@lab9.route('/lab9/reset', methods=['POST'])
@login_required  # Только для авторизованных
def reset_gifts():
    # Очищаем открытые подарки
    session['opened'] = []
    
    # Перемешиваем поздравления заново
    shuffled = congratulations.copy()
    random.shuffle(shuffled)
    session['congrats'] = shuffled
    
    return jsonify({'success': True, 'message': 'Все подарки снова наполнены!'})