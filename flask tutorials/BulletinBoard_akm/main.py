from django.shortcuts import redirect
from flask import Flask, flash, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, TextAreaField, FileField
import os
import pymysql
from flask_bcrypt import Bcrypt
from db import mysql
from flask import jsonify
from app import app


bcrypt = Bcrypt(app)

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class loginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Login')


@app.route('/')
def login():
    return render_template('login.html', form=loginForm())


@app.route('/submitted', methods=['POST', 'GET'])
def submit():
    try:
        if request.method == 'POST':
            form = loginForm()
            email = form.email.data
            _password = form.password.data
            form.email.data = ''
            form.password.data = ''
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT email, password, type FROM user_table")
            rows = cursor.fetchall()
            resp = jsonify(rows)
            if not email:
                flash('*Email Address is required.')
            if '@' not in email:
                flash('*Should be Email Address.')
            if not _password:
                flash('*Password is required.')
            for row in rows:
                db_hash_password = row['password']
                print('hash_db_pw is {}'.format(db_hash_password))
                if row['email'] == email and bcrypt.check_password_hash(db_hash_password, _password):
                    print('it is same')
                    type = row['type']
                    print(type)
                    return render_template('dashboard.html', type=type)
            resp.status_code = 200
            if email and _password:
                flash('*Incorrect Email or Passowrd.')
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
        #_name = 'admin'
        #_email = 'admin@gmail.com'
        #_password = 'admin123'
        #_id = 1
        _name = 'jame'
        _email = 'jamen@gmail.com'
        _password = 'jame123'
        _id = 2
        # validate the received values
        if True:
            # do not save password as a plain text
            _hashed_password = bcrypt.generate_password_hash(_password)
            # save edits
            #sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
            #data = (_name, _email, _hashed_password,)
            sql = "INSERT INTO user_table(`id`, `name`, `email`, `password`, `profile`, `type`, `phone`, `address`, `dob`, `create_user_id`, `updated_user_id`, `deleted_user_id`, `created_at`, `updated_at`, `deleted_at`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
        cursor.execute("SELECT email FROM user_table")
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
            password FROM user_table")
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
            password FROM user_table WHERE id={}".format(id))
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
        _id = 1
        _type = '1'
        #_name = 'Kevin'
        #_email = 'kevin@gmail.com'
        #_password = 'kev876'
        # validate the received values
        if _id:
            # do not save password as a plain text
            #_hashed_password = generate_password_hash(_password)
            # save edits
            sql = "UPDATE user_table SET type=%s WHERE id=%s"
            data = (_type, _id,)
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
        cursor.execute("DELETE FROM user_table WHERE id={}".format(id))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


class userForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email Address')
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')
    type = StringField('Type')
    phone = StringField('Phone')
    date = DateField('Date Of Birth')
    address = TextAreaField('Address')
    profile = FileField('Profile')
    confirm_btn = SubmitField('Confirm')
    clear_btn = SubmitField('Clear')
    create_btn = SubmitField('Create')
    cancel_btn = SubmitField('Cancel')


@app.route('/add_user')
def new_user():
    return render_template('user_create.html', form=userForm())


@app.route('/user_create_page', methods=['POST', 'GET'])
def user_create_page():
    try:
        form = userForm()
        if form:
            print('there is form')
        if request.method == 'POST':
            print('This is Post method')
        if request.method == 'POST' and form.validate_on_submit() and form.confirm_btn.data:
            print('It pass!')
            _user_name = form.name.data
            _user_email = form.email.data
            _user_password = form.password.data
            _confirm_password = form.confirm_password.data
            _type = form.type.data
            _phone = form.phone.data
            _date = form.date.data
            _address = form.address.data
            _profile = form.profile.data
            print(_user_name)
            return render_template('show_form.html', _user_name=_user_name,
                                   _user_email=_user_email,
                                   _user_password=_user_password,
                                   _confirm_password=_confirm_password,
                                   _type=_type,
                                   _phone=_phone, _date=_date,
                                   _address=_address, _profile=_profile,
                                   form=userForm())
        elif request.method == 'POST' and form.validate_on_submit() and form.clear_btn.data:
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
            form.confirm_password.data = ''
            form.type.data = ''
            form.phone.data = ''
            form.date.data = ''
            form.address.data = ''
            form.profile.data = ''
            return render_template('show_form.html', form=userForm())
        return render_template('user_create.html', form=userForm())
    except Exception as e:
        print(e)


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
