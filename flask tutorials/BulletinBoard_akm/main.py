from flask import Flask, flash, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import PasswordInput
import os
import pymysql
from flask_bcrypt import Bcrypt
from db import mysql
from flask import jsonify
from app import app
from werkzeug.security import generate_password_hash


bcrypt = Bcrypt(app)

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class loginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = StringField('Password', widget=PasswordInput(hide_value=True))
    submit = SubmitField('Submit')


@app.route('/')
def login():
    return render_template('login.html', form=loginForm())


@app.route('/submitted', methods=['POST', 'GET'])
def submit():
    try:
        if request.method == 'POST':
            form = loginForm()
            email = form.email.data
            password = form.password.data
            form.email.data = ''
            form.password.data = ''
            #hash_password = generate_password_hash(password)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT email, password, type FROM bulletinboard")
            rows = cursor.fetchall()
            resp = jsonify(rows)
            for row in rows:
                db_hash_password = row['password']
                print(row['email'], row['password'])
                if row['email'] == email and db_hash_password == password:
                    print('it is same')
                    type = row['type']
                    print(type)
                    return render_template('dashboard.html', type=type)
            resp.status_code = 200
            flash('Invalid Credentials!')
            return render_template('login.html', form=form)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/add')
def add_user():
    try:
        #_json = request.json
        _name = 'kane'
        _email = 'kane@gmail.com'
        _password = 'kane432'
        _id = 4
        # validate the received values
        if True:
            # do not save password as a plain text
            _hashed_password = generate_password_hash(_password)
            # save edits
            #sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
            #data = (_name, _email, _hashed_password,)
            sql = "INSERT INTO bulletinboard(`id`, `name`, `email`, `password`, `profile`, `type`, `phone`, `address`, `dob`, `create_user_id`, `updated_user_id`, `deleted_user_id`, `created_at`, `updated_at`, `deleted_at`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            #data = (_name, _email, _hashed_password,)
            data = (_id, _name, _email, _hashed_password, 'de4', '0', '09234551', 'ygn', '2001-09-24', 3, 4, 5, '2011-03-02', '2022-01-01', '2022-02-09')
            print(data)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/email')
def email():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT email FROM bulletinboard")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        for row in rows:
            print(row["email"])
        print(rows)
        resp.status_code = 200
        return jsonify(rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users')
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, \
            password FROM bulletinboard")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        print(rows)
        resp.status_code = 200
        return jsonify(rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/user/<int:id>')
def user(id):
    try:
        print(id)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, \
            password FROM bulletinboard WHERE id={}".format(id))
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return jsonify(rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update')
def update_user():
    try:
        #_json = request.json
        _id = 2
        _type = 0
        _name = 'Kevin'
        _email = 'kevin@gmail.com'
        _password = 'kev876'
        # validate the received values
        if _name and _email and _password and _id:
            # do not save password as a plain text
            _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "UPDATE bulletinboard SET name=%s, email=%s, \
                password=%s, type=%s WHERE id=%s"
            data = (_name, _email, _hashed_password, _type, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<int:id>')
def delete_user(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bulletinboard WHERE id={}".format(id))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run(debug=True)
