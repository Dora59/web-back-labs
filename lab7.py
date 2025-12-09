from flask import Blueprint, render_template, request, jsonify, abort
from datetime import datetime 
import psycopg2 
from psycopg2.extras import RealDictCursor

lab7 = Blueprint('lab7', __name__)

def get_db():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='darya_pyatina_knowledge_base',
        user='darya_pyatina_knowledge_base',
        password='777'
    )
    return conn

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM films ORDER BY id')
    films = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM films WHERE id = %s', (id,))
    film = cur.fetchone()
    cur.close()
    conn.close()
    
    if not film:
        abort(404, description=f"Фильм с ID {id} не найден")
    return jsonify(film)

@lab7.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found", "message": str(error.description)}), 404

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute('SELECT * FROM films WHERE id = %s', (id,))
    film = cur.fetchone()
    
    if not film:
        cur.close()
        conn.close()
        abort(404, description=f"Фильм с ID {id} не найден")
    
    cur.execute('DELETE FROM films WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    
    # Проверка русского названия
    if not film.get('title_ru') or film.get('title_ru', '').strip() == '':
        return jsonify({'title_ru': 'Введите русское название'}), 400
    
    # Проверка года
    current_year = datetime.now().year
    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > current_year:
            return jsonify({'year': f'Год должен быть от 1895 до {current_year}'}), 400
    except (ValueError, TypeError):
        return jsonify({'year': 'Введите корректный год'}), 400

    # Проверка описания
    description = film.get('description', '')
    if not description or description.strip() == '':
        return jsonify({'description': 'Заполните описание'}), 400
    if len(description) > 2000:
        return jsonify({'description': 'Описание не должно превышать 2000 символов'}), 400
    
    # Автозаполнение английского названия
    if not film.get('title') and film.get('title_ru'):
        film['title'] = film['title_ru']
    
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Проверяем существование фильма
    cur.execute('SELECT id FROM films WHERE id = %s', (id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        abort(404, description=f"Фильм с ID {id} не найден")
    
    # Обновляем
    cur.execute('''
        UPDATE films 
        SET title = %s, title_ru = %s, year = %s, description = %s
        WHERE id = %s
        RETURNING *
    ''', (film.get('title'), film['title_ru'], film['year'], film['description'], id))
    
    updated_film = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify(updated_film)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    # Проверка русского названия
    if not film.get('title_ru') or film.get('title_ru', '').strip() == '':
        return jsonify({'title_ru': 'Введите русское название'}), 400
    
    # Проверка года
    current_year = datetime.now().year
    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > current_year:
            return jsonify({'year': f'Год должен быть от 1895 до {current_year}'}), 400
    except (ValueError, TypeError):
        return jsonify({'year': 'Введите корректный год'}), 400
    
    # Проверка описания
    description = film.get('description', '')
    if not description or description.strip() == '':
        return jsonify({'description': 'Заполните описание'}), 400
    if len(description) > 2000:
        return jsonify({'description': 'Описание не должно превышать 2000 символов'}), 400
    
    # Автозаполнение английского названия
    if not film.get('title') and film.get('title_ru'):
        film['title'] = film['title_ru']

    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute('''
        INSERT INTO films (title, title_ru, year, description)
        VALUES (%s, %s, %s, %s)
        RETURNING *
    ''', (film.get('title'), film['title_ru'], film['year'], film['description']))
    
    new_film = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify(new_film)