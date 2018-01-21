from flask import Flask, render_template, jsonify, request, redirect
import json
from textwrap import dedent
from uuid import uuid4
from blockchain import BlockChain
from datetime import datetime
from flask.ext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'change plz'
app.config['MYSQL_DATABASE_DB'] = 'accountBook'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def home_intro():
    return render_template('intro.html', name="home_intro")

@app.route('/current')
def current():
    return render_template('current.html', name="current")

@app.route('/home')
def home_main():
    return render_template('home.html', name="home_main")


@app.route('/addAccount', methods=['POST'])
def addAcount():
    try:
        _use_name = request.form['use_name']
        _use_description = request.form['use_d']
        _use_money = int(request.form['use_money'])
        _use_date = int(request.form['use_date'])
        _write_name = 'writer'
        _write_date = 20180101
        print(type(_write_date))

        conn = mysql.connect()
        cursor = conn.cursor()
        print((_use_name, _use_description, _use_money, _use_date, _write_date, _write_name))
        print((type(_use_name), type(_use_description), type(_use_money), type(_use_date), type(_write_date), type(_write_name)))
        cursor.callproc('sp_addAccount', (_use_name, _use_description, _use_money, _use_date, _write_date, _write_name))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return redirect('/home')
        else:
            return render_template('error.html', error='An error occurred!')

    except Exception as e:
        print(str(e))
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/stat')
def stat():
    return render_template('stat.html', name="stat")

@app.route('/join')
def join():
    return render_template('join.html', name="join")


if __name__ == '__main__':
    app.run()
