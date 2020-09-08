from flask import Flask, redirect, url_for, render_template, request
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main_view():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT * FROM balance;')
    balance = cur.fetchone()[1]
    formatted_balance = f'{balance:,}'
    cur.close()
    conn.close()
    return render_template('base.html',
                            balance=balance,
                            formatted_balance=formatted_balance)

@app.route('/transact', methods=['POST'])
def submit():
    print(f'Form fields: {request.form}')
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    existing_balance = request.form['existing_balance']
    deposit_amount = request.form['deposit_amount']
    new_balance = int(existing_balance) + int(deposit_amount)
    key = request.form['idempotency_key']

    # Here we make sure we don't update the account balance if the idempotency feature is set
    # and the key has been used already
    if key != '':
        cur.execute(f'SELECT * FROM idempotency_keys WHERE key = \'{key}\';')
        existing_key = cur.fetchone()
        # UPDATE THIS TO LOGGING PROTOCOL IF NEEDED
        print(f'Database record for this key: {existing_key}')
        # If the key is found in the db, don't update...
        if existing_key is not None:
            cur.close()
            conn.close()
            return redirect(url_for('main_view'))
        # ...but if not, add it to the db and update the account balance.
        else:
            cur.execute(f'UPDATE balance SET universal_balance = {new_balance};\
                          INSERT into idempotency_keys (key) VALUES (\'{key}\');')
    # No idempotency key set, so update the balance
    else:
        cur.execute(f'UPDATE balance SET universal_balance = {new_balance};')
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('main_view'))
