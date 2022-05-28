from flask import Flask, flash, render_template, request, session, redirect
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField,\
    TextAreaField, FileField, SelectField
import os
import pymysql
from flask_bcrypt import Bcrypt
from db import mysql
from flask import jsonify
from app import app
from datetime import datetime
import dateutil.parser


bcrypt = Bcrypt(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class loginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Login')


class userForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email Address')
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')
    type = SelectField('Type', choices=[('1', 'Admin'), ('0', 'User')])
    phone = StringField('Phone')
    date = DateField('Date Of Birth')
    address = TextAreaField('Address')
    profile = FileField('Profile')
    confirm_btn = SubmitField('Confirm')
    confirm_update_btn = SubmitField('Confirm ')
    clear_btn = SubmitField('Clear')
    update_clear_btn = SubmitField('Clear')
    create_btn = SubmitField('Create')
    update_create_btn = SubmitField('Update')
    cancel_btn = SubmitField('Cancel')
    update_cancel_btn = SubmitField('Cancel')


# Home page/ login page


@app.route('/')
def login():
    return render_template('login.html', form=loginForm())


@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', form=loginForm())

# After pressing "login" button this API will work


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
            cursor.execute("SELECT id, name, email, password,\
                            type FROM user_table")
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
                if row['email'] == email and \
                   bcrypt.check_password_hash(db_hash_password, _password):
                    print('it is same')
                    type = row['type']
                    print(type)
                    session['name'] = row['name']
                    session['id'] = row['id']
                    session['type'] = row['type']
                    current_name = session.get('name')
                    print("you save the current name \
in session {}".format(current_name))
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


@app.route('/users', methods=['POST', 'GET'])
def users():
    # if request.method == 'POST':
    if True:
        try:
            current_name = session.get('name')
            current_type = session.get('type')
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM user_table")
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            # return jsonify(rows)
            print(current_type)
            return render_template('users_list.html', rows=rows,
                                   current_name=current_name,
                                   current_type=current_type)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    # return not_found()


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.form['search']:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            current_name = session.get('name')
            current_type = session.get('type')
            if request.form['user_name'] and request.form['user_email'] and\
               request.form['from_date'] and request.form['to_date']:
                _user_name = request.form.get('user_name')
                _user_email = request.form.get('user_email')
                _raw_from_date = request.form.get('from_date')
                _raw_to_date = request.form.get('to_date')
                # 'Sun, 01 May 2022 00:00:00 GMT'
                # to change this format to %Y-%m-%d
                date1 = dateutil.parser.parse(_raw_from_date)
                date2 = dateutil.parser.parse(_raw_to_date)
                _from_date = date1.strftime('%Y-%m-%d')
                _to_date = date2.strftime('%Y-%m-%d')
                print(_from_date)
                print(_to_date)
                sql = "SELECT * FROM user_table WHERE created_at>=%s OR\
                    created_at<=%s OR name=%s OR email=%s;"
                data = (_from_date, _to_date, _user_name, _user_email)
                cursor.execute(sql, data)
                rows = cursor.fetchall()
                resp = jsonify(rows)
                resp.status_code = 200
                # return jsonify(rows)
                return render_template('users_list.html', rows=rows,
                                       current_name=current_name,
                                       current_type=current_type)
            if request.form['user_name'] and request.form['user_email'] and\
               request.form['from_date']:
                _user_name = request.form.get('user_name')
                _user_email = request.form.get('user_email')
                _raw_from_date = request.form.get('from_date')
                # 'Sun, 01 May 2022 00:00:00 GMT'
                # to change this format to %Y-%m-%d
                date1 = dateutil.parser.parse(_raw_from_date)
                _from_date = date1.strftime('%Y-%m-%d')
                sql = "SELECT * FROM user_table WHERE created_at>=%s OR\
                    name=%s OR email=%s;"
                data = (_from_date, _user_name, _user_email)
                cursor.execute(sql, data)
                rows = cursor.fetchall()
                resp = jsonify(rows)
                resp.status_code = 200
                # return jsonify(rows)
                return render_template('users_list.html', rows=rows,
                                       current_name=current_name,
                                       current_type=current_type)
            if request.form['user_name'] and request.form['user_email'] and\
               request.form['to_date']:
                _user_name = request.form.get('user_name')
                _user_email = request.form.get('user_email')
                _raw_to_date = request.form.get('to_date')
                # 'Sun, 01 May 2022 00:00:00 GMT'
                # to change this format to %Y-%m-%d
                date1 = dateutil.parser.parse(_raw_to_date)
                _to_date = date1.strftime('%Y-%m-%d')
                sql = "SELECT * FROM user_table WHERE created_at<=%s OR\
                    name=%s OR email=%s;"
                data = (_to_date, _user_name, _user_email)
                rows = cursor.fetchall()
                resp = jsonify(rows)
                resp.status_code = 200
                # return jsonify(rows)
                return render_template('users_list.html', rows=rows,
                                       current_name=current_name,
                                       current_type=current_type)
            if request.form['user_name'] and request.form['user_email']:
                _user_name = request.form.get('user_name')
                _user_email = request.form.get('user_email')
                sql = "SELECT * FROM user_table WHERE name=%s OR email=%s;"
                data = (_user_name, _user_email)
                cursor.execute(sql, data)
                rows = cursor.fetchall()
                resp = jsonify(rows)
                resp.status_code = 200
                # return jsonify(rows)
                return render_template('users_list.html', rows=rows,
                                       current_name=current_name,
                                       current_type=current_type)
            if request.form['user_name']:
                _user_name = request.form.get('user_name')
                print('this is search check point')
                sql = "SELECT * FROM user_table WHERE `name`=%s;"
                data = (_user_name)
                cursor.execute(sql, data)
                rows = cursor.fetchall()
                resp = jsonify(rows)
                resp.status_code = 200
                # return jsonify(rows)
                return render_template('users_list.html', rows=rows,
                                       current_name=current_name,
                                       current_type=current_type)
            if request.form['user_email']:
                _user_email = request.form.get('user_email')
                sql = "SELECT * FROM user_table WHERE `email`=%s;"
                data = (_user_email)
                cursor.execute(sql, data)
                rows = cursor.fetchall()
                resp = jsonify(rows)
                resp.status_code = 200
                # return jsonify(rows)
                return render_template('users_list.html', rows=rows,
                                       current_name=current_name,
                                       current_type=current_type)
            if request.form['from_date']:
                _raw_from_date = request.form.get('from_date')
                # 'Sun, 01 May 2022 00:00:00 GMT'
                # to change this format to %Y-%m-%d
                date1 = dateutil.parser.parse(_raw_from_date)
                _from_date = date1.strftime('%Y-%m-%d')
                sql = "SELECT * FROM user_table WHERE created_at>= %s;"
                data = (_from_date)
                cursor.execute(sql, data)
                rows = cursor.fetchall()
                resp = jsonify(rows)
                resp.status_code = 200
                # return jsonify(rows)
                return render_template('users_list.html', rows=rows,
                                       current_name=current_name,
                                       current_type=current_type)
            if request.form['to_date']:
                _raw_to_date = request.form.get('to_date')
                # 'Sun, 01 May 2022 00:00:00 GMT'
                # to change this format to %Y-%m-%d
                date2 = dateutil.parser.parse(_raw_to_date)
                _to_date = date2.strftime('%Y-%m-%d')
                sql = "SELECT * FROM user_table WHERE created_at <= %s;"
                data = (_to_date)
                cursor.execute(sql, data)
                rows = cursor.fetchall()
                resp = jsonify(rows)
                resp.status_code = 200
                # return jsonify(rows)
                return render_template('users_list.html', rows=rows,
                                       current_name=current_name,
                                       current_type=current_type)
            else:
                return redirect('/users')
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
        cursor.execute("SELECT * FROM user_table WHERE id={}".format(id))
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update_user(id):
    try:
        print(id)
        current_name = session.get('name')
        form = userForm()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user_table WHERE id={}".format(id))
        row = cursor.fetchone()
        _name = row['name']
        _email = row['email']
        if row['type'] == '1':
            _type = 'Admin'
        else:
            _type = 'User'
        _phone = row['phone']
        _date = row['dob']
        _address = row['address']
        _profile = row['profile']
        userForm.address = TextAreaField('Address', default=_address)
        if form.confirm_update_btn.data and form.validate_on_submit() and\
           request.method == "POST":
            print('this is in update It pass!')
            _user_name = form.name.data
            session['input_name'] = _user_name
            _user_email = form.email.data
            session['input_email'] = _user_email
            _type = form.type.data
            session['input_type'] = _type
            _phone = form.phone.data
            session['input_phone'] = _phone
            _date = form.date.data
            session['input_date'] = _date
            _address = form.address.data
            session['input_address'] = _address
            _profile = form.profile.data
            session['input_profile'] = _profile
            name_error = None
            email_requ_error = None
            not_email_error = None
            phone_error = None
            date_error = None
            cannot_insert = False
            print('check empty!')
            if not _user_name:
                name_error = '*Name is required'
                cannot_insert = True
                print('no name')
            if not _user_email:
                email_requ_error = '*Email address is required.'
                cannot_insert = True
                print('email required')
            if '@' not in _user_email:
                not_email_error = '*Should be email format.'
                cannot_insert = True
                print('not email')
            min_num = '09200000000'
            max_num = '09999999999'
            if not _phone or not _phone.isdigit() or\
               int(_phone) < int(min_num) or int(_phone) > int(max_num):
                phone_error = '*Phone is required.It needs to be\
only number contains 11 digits. (09xxxxxxxxx)!'
                cannot_insert = True
            _input_date = datetime.strptime(str(_date), "%Y-%m-%d")
            present = datetime.now()
            if _input_date > present:
                date_error = 'Date of birth is bigger than today date.'
                cannot_insert = True
            if cannot_insert:
                return render_template(
                    'update_page.html', name_error=name_error,
                    email_requ_error=email_requ_error,
                    not_email_error=not_email_error,
                    phone_error=phone_error, date_error=date_error,
                    form=userForm(),
                    current_name=current_name)
            if _type == '0':
                _for_user_type = 'User'
            else:
                _for_user_type = 'Admin'
            #my_file = _profile
            #print(my_file)
            #path = os.getcwd()
            #folder_name = r'\temporary'
            #folder_to_save_files = path + folder_name
            #if not os.path.exists(folder_to_save_files):
            #    os.mkdir(folder_to_save_files)
            #print(folder_to_save_files)
            #my_file.save(os.path.join(folder_to_save_files, my_file.filename))
            #print(folder_to_save_files)
            #_temp_profile = url_for('temporary', filename=_profile)
            #print(_temp_profile)
            return render_template('update_show_form.html',
                                   _user_name=_user_name,
                                   _user_email=_user_email,
                                   _type=_for_user_type,
                                   _phone=_phone, _date=_date,
                                   _address=_address, _profile=_profile,
                                   form=userForm(), current_name=current_name)
        elif (request.method == 'POST' and
              form.clear_btn.data):
            form.name.data = ""
            form.email.data = ""
            form.password.data = ""
            form.confirm_password.data = ""
            form.type.data = ""
            form.phone.data = ""
            form.date.data = ""
            form.address.data = ""
            form.profile.data = ""
            print("Clear btn")
            print(form.name.data)
            return render_template(
                    'update_page.html',
                    form=form,
                    current_name=current_name)
        if request.method == 'POST' and form.update_create_btn.data:
            _user_name = session.get('input_name')
            _user_email = session.get('input_email')
            _profile = session.get('input_profile')
            _type = session.get('input_type')
            _phone = session.get('input_phone')
            _address = session.get('input_address')
            _raw_date = session.get('input_date')
            # 'Sun, 01 May 2022 00:00:00 GMT' to change this format to %Y-%m-%d
            dt = dateutil.parser.parse(_raw_date)
            _date = dt.strftime('%Y-%m-%d')
            print(_date)
            print('pressed Create ')
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d|%H:%M:%S")
            _profile = 'rre21'
            _update_user_id = session.get('id')
            _update_at = current_time
            _id = id
            sql = "UPDATE user_table SET name=%s, email=%s, profile=%s,\
                type=%s, phone=%s, address=%s, dob=%s, updated_user_id=%s,\
                    updated_at=%s WHERE id=%s"
            data = (_user_name, _user_email, _profile,
                    _type, _phone, _address, _date,
                    _update_user_id, _update_at, _id)
            print(data)
            print(_date)
            cursor.execute(sql, data)
            conn.commit()
            return redirect('/users')
        return render_template('update_page.html', _name=_name,
                               _email=_email, _type=_type,
                               _phone=_phone, _date=_date,
                               _address=_address, _profile=_profile,
                               form=form)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#@app.route('/delete/<int:id>')
#def delete_user(id):
#    try:
#        conn = mysql.connect()
#        cursor = conn.cursor()
#        cursor.execute("DELETE FROM user_table WHERE id={}".format(id))
#        conn.commit()
#        resp = jsonify('User deleted successfully!')
#        resp.status_code = 200
#        return resp
#    except Exception as e:
#        print(e)
#    finally:
#        cursor.close()
#        conn.close()
# To create user after pressing "Create User For Admin" button


@app.route('/user_create_page', methods=['POST', 'GET'])
def user_create_page():
    try:
        form = userForm()
        current_name = session.get("name")
        if request.method == 'POST' and\
           form.confirm_btn.data:
            print('It pass!')
            _user_name = form.name.data
            session['input_name'] = _user_name
            _user_email = form.email.data
            session['input_email'] = _user_email
            _user_password = form.password.data
            session['input_password'] = _user_password
            _confirm_password = form.confirm_password.data
            _type = form.type.data
            session['input_type'] = _type
            _phone = form.phone.data
            session['input_phone'] = _phone
            _date = form.date.data
            session['input_date'] = _date
            _address = form.address.data
            session['input_address'] = _address
            _profile = form.profile.data
            session['input_profile'] = _profile
            name_error = None
            email_requ_error = None
            not_email_error = None
            password_equal_error = None
            password_format_error = None
            phone_error = None
            cannot_insert = False
            print('check empty!')
            if not _user_name:
                name_error = '*Name is required'
                cannot_insert = True
                print('no name')
            if not _user_email:
                email_requ_error = '*Email address is required.'
                cannot_insert = True
                print('email required')
            if '@' not in _user_email:
                not_email_error = '*Should be email format.'
                cannot_insert = True
                print('not email')
            if _user_password != _confirm_password:
                password_equal_error = '*Password and confirm password \
must be same.'
                cannot_insert = True
                print('pw and con-pw not same')

            def include_num(x_string):
                for i in x_string:
                    if i.isdigit():
                        return True
                return False

            def has_uppercase(y_string):
                for j in y_string:
                    if j.isupper():
                        return True
                return False
            if len(_user_password) < 9 or not include_num(_user_password) or\
               not has_uppercase(_user_password):
                password_format_error = '*Password must be more than \
8 characters long, must conatain 1 Uppercase and 1 Numeric.'
                cannot_insert = True
            _user_password_dots = len(_user_password) * '*'
            min_num = '09200000000'
            max_num = '09999999999'
            if not _phone or not _phone.isdigit() or\
               int(_phone) < int(min_num) or int(_phone) > int(max_num):
                phone_error = '*Phone is required.It needs to be\
only number contains 11 digits. (09xxxxxxxxx)!'
                cannot_insert = True
            _input_date = datetime.strptime(str(_date), "%Y-%m-%d")
            present = datetime.now()
            if _input_date > present:
                date_error = 'Date of birth is bigger than today date.'
                cannot_insert = True
            if cannot_insert:
                return render_template(
                    'user_create.html', name_error=name_error,
                    email_requ_error=email_requ_error,
                    not_email_error=not_email_error,
                    password_equal_error=password_equal_error,
                    password_format_error=password_format_error,
                    phone_error=phone_error, date_error=date_error,
                    form=userForm(),
                    current_name=current_name)
            if _type == '0':
                _for_user_type = 'User'
            else:
                _for_user_type = 'Admin'
            #my_file = _profile
            #print(my_file)
            #path = os.getcwd()
            #folder_name = r'\temporary'
            #folder_to_save_files = path + folder_name
            #if not os.path.exists(folder_to_save_files):
            #    os.mkdir(folder_to_save_files)
            #print(folder_to_save_files)
            #my_file.save(os.path.join(folder_to_save_files, my_file.filename))
            #print(folder_to_save_files)
            #_temp_profile = url_for('temporary', filename=_profile)
            #print(_temp_profile)
            return render_template('show_form.html', _user_name=_user_name,
                                   _user_email=_user_email,
                                   _user_password=_user_password_dots,
                                   _confirm_password=_confirm_password,
                                   _type=_for_user_type,
                                   _phone=_phone, _date=_date,
                                   _address=_address, _profile=_profile,
                                   form=userForm(), current_name=current_name)
        elif (request.method == 'POST' and
              form.clear_btn.data):
            form.name.data = ""
            form.email.data = ""
            form.password.data = ""
            form.confirm_password.data = ""
            form.type.data = ""
            form.phone.data = ""
            form.date.data = ""
            form.address.data = ""
            form.profile.data = ""
            print("Clear btn")
            print(form.name.data)
            return render_template(
                    'user_create.html',
                    form=form,
                    current_name=current_name)
        if request.method == 'POST' and form.create_btn.data:
            _user_name = session.get('input_name')
            _user_email = session.get('input_email')
            _user_password = session.get('input_password')
            _profile = session.get('input_profile')
            _type = session.get('input_type')
            _phone = session.get('input_phone')
            _address = session.get('input_address')
            _raw_date = session.get('input_date')
            # 'Sun, 01 May 2022 00:00:00 GMT' to change this format to %Y-%m-%d
            dt = dateutil.parser.parse(_raw_date)
            _date = dt.strftime('%Y-%m-%d')
            print(_date)
            print('pressed Create ')
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id, name, email, password,\
                type FROM user_table")
            rows = cursor.fetchall()
            email_exist_error = None
            for row in rows:
                print(_user_email)
                print("Email check point")
                print(row['email'])
                if _user_email == row['email']:
                    email_exist_error = 'User with this email exist'
                    return render_template('user_create.html',
                                           form=userForm(),
                                           email_exist_error=email_exist_error,
                                           current_name=current_name)
            print("Email passed")
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d|%H:%M:%S")
            last_row = rows[len(rows)-1]
            _id = last_row['id'] + 1
            _hashed_password = bcrypt.generate_password_hash(_user_password)
            _profile = 'rre21'
            _create_user_id = session.get('id')
            _update_user_id = session.get('id')
            _create_at = current_time
            _update_at = current_time
            sql = "INSERT INTO user_table(`id`, `name`, `email`, `password`,\
                `profile`, `type`, `phone`, `address`, `dob`, \
                    `create_user_id`, `updated_user_id`, `deleted_user_id`,\
                        `created_at`, `updated_at`,\
                            `deleted_at`) VALUES(%s, %s, %s, %s,\
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (_id, _user_name, _user_email, _hashed_password, _profile,
                    _type, _phone, _address, _date, _create_user_id,
                    _update_user_id, None, _create_at, _update_at, None)
            print(data)
            print(_date)
            cursor.execute(sql, data)
            conn.commit()
            return redirect('/users')
        return render_template('user_create.html', form=userForm(),
                               current_name=current_name)
    except Exception as e:
        print(e)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        # 'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run(debug=True)
