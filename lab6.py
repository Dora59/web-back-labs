from flask import Blueprint, request, render_template, redirect, session, current_app
import random
import psycopg2 
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
lab6 = Blueprint('lab6', __name__)

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

# функции подключения к БД и отключения
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='darya_pyatina_knowledge_base',
            user='darya_pyatina_knowledge_base',
            password='777',
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    # Подключаемся к БД
    conn, cur = db_connect()
    
    try:
        if data['method'] == 'info':
            # Получаем данные ИЗ БАЗЫ ДАННЫХ
            cur.execute('SELECT * FROM offices ORDER BY number')
            offices_db = cur.fetchall()
            
            offices_list = []
            for office in offices_db:
                offices_list.append({
                    'number': office['number'],
                    'tenant': office['tenant'] or '',
                    'price': office['price']
                })
            
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'result': offices_list,
                'id': id
            }
        
        login = session.get('login')
        if not login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }
        
        if data['method'] == 'booking':
            office_number = data['params'][0]
            
            # Проверяем в БАЗЕ ДАННЫХ
            cur.execute('SELECT * FROM offices WHERE number = %s', (office_number,))
            office = cur.fetchone()
            
            if not office:
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 5,
                        'message': 'Office not found'
                    },
                    'id': id
                }
            
            if office['tenant']:  # Если офис уже занят
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 2,
                        'message': 'Already booked'
                    },
                    'id': id
                }
            
            # Обновляем в БАЗЕ ДАННЫХ
            cur.execute(
                'UPDATE offices SET tenant = %s WHERE number = %s',
                (login, office_number)
            )
            db_close(conn, cur)
            
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }

        if data['method'] == 'cancellation': 
            office_number = data['params'][0]
            
            # Проверяем в БАЗЕ ДАННЫХ
            cur.execute('SELECT * FROM offices WHERE number = %s', (office_number,))
            office = cur.fetchone()
            
            if not office:
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 5,
                        'message': 'Office not found'
                    },
                    'id': id
                }
            
            if not office['tenant']:
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 3,
                        'message': 'Office is not booked'
                    },
                    'id': id
                }
            
            if office['tenant'] != login:
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 4,
                        'message': 'You can only cancel your own booking'
                    },
                    'id': id
                }
            
            # Обновляем в БАЗЕ ДАННЫХ
            cur.execute(
                'UPDATE offices SET tenant = %s WHERE number = %s',
                ('', office_number)
            )
            db_close(conn, cur)
            
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }

        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Method not found'
            },
            'id': id
        }
    
    except Exception as e:
        # Обработка ошибок БД
        conn.rollback()
        db_close(conn, cur)
        print(f"Database error: {e}")
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32603,
                'message': 'Internal server error'
            },
            'id': id
        }