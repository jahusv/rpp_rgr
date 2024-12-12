from flask import Blueprint, render_template, request, redirect, Flask
import psycopg2

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:@{host}/{database}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'my_secret_key'  

    app.register_blueprint(rgr)

    return app

# Определяем Blueprint с именем 'rgr'
rgr = Blueprint('rgr', __name__)

def dbConnect():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database='rgr',
        user='sajfulina_alina'
    )
    return conn

def dbClose(cursor, connection):
    cursor.close()
    connection.close()

# Главная страница с отображением всех подписок
@rgr.route('/', methods=['GET'])
def main():
    conn = dbConnect()
    cur = conn.cursor()
    cur.execute("""select subscription_id, name, cost, frequency, start_date from subscriptions""")
    subscriptions = cur.fetchall()
    dbClose(cur, conn)
    return render_template('index.html', subscriptions=subscriptions)

# Страница добавления подписки
@rgr.route('/add_subscription')
def add_subscription():
    return render_template('adding.html')

# Сохранение новой подписки
@rgr.route('/save_subscription', methods=['POST'])
def save_subscription():
    name = request.form['name']
    cost = request.form['cost']
    frequency = request.form['frequency']
    start_date = request.form['start_date']

    conn = dbConnect()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO subscriptions (name, cost, frequency, start_date)
    VALUES (%s, %s, %s, %s)
    """, (name, cost, frequency, start_date))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

# Страница редактирования подписки
@rgr.route('/edit_subscription/<int:subscription_id>', methods=['GET'])
def edit_subscription(subscription_id):
    conn = dbConnect()
    cur = conn.cursor()
    cur.execute("SELECT subscription_id, name, cost, frequency, start_date FROM subscriptions WHERE subscription_id = %s", (subscription_id,))
    subscription = cur.fetchone()
    dbClose(cur, conn)
    if subscription:
        return render_template('edit.html', subscription=subscription)
    else:
        return "Подписка не найдена", 404

# Обновление подписки
@rgr.route('/update_subscription/<int:subscription_id>', methods=['POST'])
def update_subscription(subscription_id):
    name = request.form['name']
    cost = request.form['cost']
    frequency = request.form['frequency']
    start_date = request.form['start_date']

    conn = dbConnect()
    cur = conn.cursor()
    cur.execute("""
    UPDATE subscriptions
    SET name = %s, cost = %s, frequency = %s, start_date = %s
    WHERE subscription_id = %s
    """, (name, cost, frequency, start_date, subscription_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

# Удаление подписки
@rgr.route('/delete_subscription/<int:subscription_id>')
def delete_subscription(subscription_id):
    conn = dbConnect()
    cur = conn.cursor()
    cur.execute("DELETE FROM subscriptions WHERE subscription_id = %s", (subscription_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
