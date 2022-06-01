from flask import Flask, flash, render_template, request, session, redirect
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField,\
    TextAreaField, FileField, SelectField
import os, shutil
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

# If running with others PC filepath always needs to be check and must have the path like following
# 'path + \flask tutorials\BulletinBoard_akm\static\temporary'
path = os.getcwd()
next_folder = r'\flask tutorials'
bulletin_folder = r'\BulletinBoard_akm'
static_folder = r'\static'
folder_name = r'\temporary'
first_folder = path + next_folder + bulletin_folder + static_folder
if not os.path.exists(first_folder):
    os.mkdir(first_folder)
folder_to_save_files = first_folder + folder_name
UPLOAD_FOLDER = folder_to_save_files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


class postForm(FlaskForm):
    post_title = StringField('Title')
    post_description = TextAreaField('Description')
    confirm_post = SubmitField('Confirm')
    clear_post = SubmitField('Clear')
    create_post = SubmitField('Create')
    cancel_post = SubmitField('Cancel')
    update_confirm_post = SubmitField('Confirm')
    update_clear_post = SubmitField('Clear')
    update_create_post = SubmitField('Create')
    update_cancel_post = SubmitField('Cancel')


# Home page/ login page


@app.route('/')
def login():
    return render_template('login.html', form=loginForm())


@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', form=loginForm())

# change the password API


@app.route('/password_change', methods=['POST', 'GET'])
def change():
    form = userForm()
    _user_password = form.password.data
    # session['input_password'] = _user_password
    _confirm_password = form.confirm_password.data
    if request.method == 'POST' and form.confirm_btn.data:
        cannot_insert = False
        password_equal_error = None
        password_format_error = None
        done = None
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
        if cannot_insert:
            return render_template('password_change.html',
                                   password_equal_error=password_equal_error,
                                   password_format_error=password_format_error,
                                   form=userForm())
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        _hashed_password = bcrypt.generate_password_hash(_user_password)
        _id = int(session.get('update_id'))
        sql = "UPDATE user_table SET password=%s WHERE id=%s"
        data = (_hashed_password, _id)
        cursor.execute(sql, data)
        conn.commit()
        print("this is id whose pw has been changed")
        print(_id)
        done = 'The password is successfully changed!'
        session['done'] = done
        session['check_once'] = 0
        return redirect('/update/{}'.format(_id))
    return render_template('password_change.html', form=userForm())


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
    print('you reached search')
    if request.form.get('search'):
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
    elif request.form.get('add'):
        return redirect('/user_create_page')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update_user(id):
    try:
        # session['chech_once'] is for showing the \
        # 'password changing is successful' only for one time
        if session.get('check_once'):
            i = session.get('check_once')
            i += 1
            session['check_once'] = i
        else:
            session['check_once'] = 2
            i = session.get('check_once')
        session['update_id'] = id
        _update_id = id
        current_name = session.get('name')
        current_id = session.get('id')
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
        _raw_profile = row['profile']
        path_list = _raw_profile.split("\\")
        _primary_profile = path_list[len(path_list) - 1]
        print("you reached to /update")
        print('the profile is: {}'.format(_primary_profile))
        _address = row['address']
        print('the address is: {}'.format(_address))
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
            # Here to change the code!
            # Also need to check in html for profile input form
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
            if _input_date > present or not _input_date:
                date_error = 'It should not be empty and date of birth is bigger than today date. '
                cannot_insert = True
            if _input_date > present or not _input_date:
                date_error = 'Date should not be empty and date of birth is bigger than today date.'
                cannot_insert = True

            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower()\
                    in ALLOWED_EXTENSIONS
            profile_has = False
            if _profile:
                print('there is profile !!!!')
                profile_has = True
                print("this is the file: {}".format(_profile))
                _file = _profile.filename
                print(_file, '  ', type(_file))
                if _file and not allowed_file(_file):
                    file_error = 'The chosen file is not valid file type. Allow\
    file type are "jpg", "png", and "jpeg"'
                    cannot_insert = True
            if cannot_insert:
                return render_template(
                    'update_page.html', name_error=name_error,
                    email_requ_error=email_requ_error,
                    not_email_error=not_email_error,
                    phone_error=phone_error, date_error=date_error,
                    _name=_name, _email=_email, _type=_type,
                    _phone=_phone, _date=_date,
                    _address=_address, _profile=_profile,
                    file_error=file_error, form=form,
                    current_name=current_name)
            if _type == '0':
                _for_user_type = 'User'
            else:
                _for_user_type = 'Admin'
            _update_id = session.get('update_id')
            if _profile:
                print(folder_to_save_files)
                print('This is the uploaded file:  {}'.format(_file))
                if not os.path.exists(folder_to_save_files):
                    os.mkdir(folder_to_save_files)
                _profile.save(os.path.join(folder_to_save_files,
                                           _profile.filename))
                print(folder_to_save_files)
                print(type(_profile))
                print("Saving is done")
                _folder_file = 'temporary/' + _file
                print(type(_file))
                session['input_profile_path'] = folder_to_save_files +\
                    r'\{}'.format(_file)
                return render_template('update_show_form.html',
                                       _user_name=_user_name,
                                       _user_email=_user_email,
                                       _type=_for_user_type,
                                       _phone=_phone, _date=_date,
                                       _folder_file=_folder_file,
                                       _address=_address, _profile=_profile,
                                       form=userForm(),
                                       profile_has=profile_has,
                                       current_name=current_name,
                                       current_id=current_id)
            return render_template('update_show_form.html',
                                   _user_name=_user_name,
                                   _user_email=_user_email,
                                   _type=_for_user_type,
                                   _phone=_phone, _date=_date,
                                   _address=_address,
                                   _primary_profile=_primary_profile,
                                   profile_has=profile_has,
                                   _update_id=_update_id,
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
            current_time = now.strftime("%Y-%m-%d")
            _profile = session.get('input_profile_path')
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
        done = session.get('done')
        print('this is the "i" value ', i)
        return render_template('update_page.html', _name=_name,
                               _email=_email, _type=_type,
                               _phone=_phone, _date=_date,
                               _address=_address,
                               _primary_profile=_primary_profile,
                               _update_id=_update_id,
                               form=form, done=done, i=i,
                               current_name=current_name)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<int:id>')
def delete_user(id):
    try:
        print('this is id', id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_table WHERE id={}".format(id))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return redirect('/users')
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


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
            # _profile = form.profile.data
            _profile = request.files['file']
            session['input_profile'] = _profile.filename
            name_error = None
            email_requ_error = None
            not_email_error = None
            password_equal_error = None
            password_format_error = None
            phone_error = None
            file_error = None
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
            if _input_date > present or not _input_date:
                date_error = 'Date should not be empty and date of birth is bigger than today date.'
                cannot_insert = True

            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower()\
                    in ALLOWED_EXTENSIONS
            print("this is the file: {}".format(_profile))
            _file = _profile.filename
            print(_file, '  ', type(_file))
            if _file and not allowed_file(_file):
                file_error = 'The chosen file is not valid file type. Allow\
file type are "jpg", "png", and "jpeg"'
                cannot_insert = True
            if cannot_insert:
                return render_template(
                    'user_create.html', name_error=name_error,
                    email_requ_error=email_requ_error,
                    not_email_error=not_email_error,
                    password_equal_error=password_equal_error,
                    password_format_error=password_format_error,
                    phone_error=phone_error, date_error=date_error,
                    file_error=file_error,
                    form=userForm(),
                    current_name=current_name)
            if _type == '0':
                _for_user_type = 'User'
            else:
                _for_user_type = 'Admin'
            print(folder_to_save_files)
            print('This is the uploaded file:  {}'.format(_file))
            if not os.path.exists(folder_to_save_files):
                os.mkdir(folder_to_save_files)
            _profile.save(os.path.join(folder_to_save_files, _profile.filename))
            print(folder_to_save_files)
            print(type(_profile))
            print("Saving is done")
            _folder_file = 'temporary/' + _file
            print(type(_file))
            session['input_profile_path'] = folder_to_save_files +\
                r'\{}'.format(_file)
            return render_template('show_form.html', _user_name=_user_name,
                                   _user_email=_user_email,
                                   _user_password=_user_password_dots,
                                   _confirm_password=_confirm_password,
                                   _type=_for_user_type,
                                   _phone=_phone, _date=_date,
                                   _address=_address, _file=_file,
                                   _folder_file=_folder_file,
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
            current_time = now.strftime("%Y-%m-%d")
            last_row = rows[len(rows)-1]
            _id = last_row['id'] + 1
            _hashed_password = bcrypt.generate_password_hash(_user_password)
            _create_user_id = session.get('id')
            _update_user_id = session.get('id')
            _create_at = current_time
            _update_at = current_time
            user_folder = r'\{}'.format(_id)
            for_user_profile = first_folder + user_folder
            print("this is the check point of user create")
            if not os.path.exists(for_user_profile):
                os.mkdir(for_user_profile)
            # _profile is filename because it got from session.
            # session cannnot accept FileStorage
            file_from_folder = session.get('input_profile_path')
            shutil.move(file_from_folder, for_user_profile)
            file_path_for_db = for_user_profile + r'\{}'.format(_profile)
            sql = "INSERT INTO user_table(`id`, `name`, `email`, `password`,\
                `profile`, `type`, `phone`, `address`, `dob`, \
                    `create_user_id`, `updated_user_id`, `deleted_user_id`,\
                        `created_at`, `updated_at`,\
                            `deleted_at`) VALUES(%s, %s, %s, %s,\
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (_id, _user_name, _user_email, _hashed_password,
                    file_path_for_db,
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


@app.route('/post_search', methods=['POST', 'GET'])
def post_search():
    if request.method == 'POST' and request.form['search']:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            current_name = session.get('name')
            current_type = session.get('type')
            print('This is the current  type: {}'.format(current_type))
            if request.form['search_item']:
                _search_item = request.form.get('search_item')
                if current_type == '0' or current_type == None:
                    sql = "SELECT * FROM post_table WHERE title=%s OR\
                    description=%s;"
                    data = (_search_item, _search_item)
                elif current_type == '1':
                    sql = "SELECT * FROM post_table WHERE title=%s OR\
                    description=%s OR create_user_id=%s;"
                    data = (_search_item, _search_item, _search_item)
                cursor.execute(sql, data)
                rows = cursor.fetchall()
                resp = jsonify(rows)
                resp.status_code = 200
                # return jsonify(rows)
                return render_template('posts_list.html', rows=rows,
                                       current_name=current_name,
                                       current_type=current_type)
            elif not request.form['search_item']:
                return redirect('/posts')
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    elif request.form['add']:
        return redirect('/user_create_page')
    elif request.form['upload']:
        return redirect('/user_create_page')


@app.route('/post_create_page', methods=['POST', 'GET'])
def add_post():
    try:
        form = postForm()
        current_name = session.get('name')
        current_type = session.get('type')
        current_id = session.get('id')
        if request.method == 'POST' and\
           form.confirm_post.data:
            print('It passed and started for post adding!')
            _post_title = form.post_title.data
            session['input_post_title'] = _post_title
            _post_description = form.post_description.data
            session['input_post_description'] = _post_description
            no_title_error = None
            long_title_error = None
            no_des_error = None
            cannot_insert = False
            if not _post_title:
                no_title_error = 'Title is required.'
                cannot_insert = True
            if len(_post_title) > 255:
                long_title_error = 'Title must be less than 255 letters.'
                cannot_insert = True
            if not _post_description:
                no_des_error = 'Description is required.'
                cannot_insert = True
            if cannot_insert:
                return render_template('post_form.html',
                                       no_title_error=no_title_error,
                                       long_title_error=long_title_error,
                                       no_des_error=no_des_error,
                                       form=postForm(),
                                       current_name=current_name,
                                       current_id=current_id,
                                       current_type=current_type)
            return render_template('show_update_post.html',
                                   _post_title=_post_title,
                                   _post_description=_post_description,
                                   form=form,
                                   current_name=current_name,
                                   current_type=current_type,
                                   current_id=current_id)
        elif (request.method == 'POST' and form.clear_post.data):
            form.post_title.data = ''
            form.post_description.data = ''
            return render_template('post_form.html', form=form,
                                   current_id=current_id,
                                   current_name=current_name)
        if request.method == 'POST' and form.create_post.data:
            _post_title = session.get('input_post_title')
            _post_description = session.get('input_post_description')
            post_exist_error = None
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM post_table")
            rows = cursor.fetchall()
            for row in rows:
                if row['title'] == _post_title:
                    post_exist_error = 'Post title already exist.'
                    return render_template('post_form.html',
                                           post_exist_error=post_exist_error,
                                           form=form,
                                           current_name=current_name,
                                           current_type=current_type,
                                           current_id=current_id)
            last_row = rows[len(rows)-1]
            _id = last_row['id'] + 1
            _status = 1
            _create_user_id = session.get('id')
            _updated_user_id = session.get('id')
            _deleted_user_id = None
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d")
            _created_at = current_time
            _updated_at = current_time
            _deleted_at = None
            sql = "INSERT INTO post_table(id, title, description, status,\
                    create_user_id, updated_user_id, deleted_user_id,\
                        created_at, updated_at, deleted_at)\
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (_id, _post_title, _post_description,
                    _status, _create_user_id,
                    _updated_user_id, _deleted_user_id, _created_at,
                    _updated_at, _deleted_at)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Post added successfully!')
            resp.status_code = 200
            return redirect('/posts')
        return render_template('post_form.html', form=postForm(),
                               current_name=current_name,
                               current_type=current_type,
                               current_id=current_id)
    except Exception as e:
        print(e)


@app.route('/posts')
def posts():
    # if request.method == 'POST':
    if True:
        try:
            current_name = session.get('name')
            current_type = session.get('type')
            current_id = session.get('id')
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM post_table")
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            # return jsonify(rows)
            print(current_type)
            return render_template('posts_list.html', rows=rows,
                                   current_name=current_name,
                                   current_type=current_type,
                                   current_id=current_id)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


@app.route('/post/<int:id>')
def post(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, title, description, status FROM post_table\
            WHERE id=%s", id)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/user_detail/<int:id>')
def user_detail(id):
    try:
        current_name = session.get('name')
        current_id = session.get('id')
        current_type = session.get('type')
        form = userForm()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user_table WHERE id={}".format(id))
        row = cursor.fetchone()
        _name = row['name']
        _email = row['email']
        _password = '***'
        _digit_type = row['type']
        if _digit_type == '1':
            _type = 'Admin'
        else:
            _type = 'User'
        _phone = row['phone']
        _dob = row['dob']
        _address = row['address']
        print('this is name: {}'. format(_name))
        typeOfid = type(current_id)
        print('this is current id: {},{}'.format(typeOfid,current_id))
        return render_template('user_detail.html', _name=_name,
                               _email=_email,
                               _password=_password,
                               _type=_type, _phone=_phone,
                               _dob=_dob, _address=_address,
                               form=form,
                               current_id=current_id,
                               current_name=current_name,
                               current_type=current_type)
    except Exception as e:
        print(e)
    

@app.route('/post_update/<int:id>', methods=['POST', 'GET'])
def update_post(id):
    try:
        current_name = session.get('name')
        current_id = session.get('id')
        current_type = session.get('type')
        form = postForm()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM post_table WHERE id={}".format(id))
        row = cursor.fetchone()
        _title = row['title']
        _description = row['description']
        print('This is the des:{}'.format(_description))
        _status = row['status']
        print('this is the status:{}'.format(_status))
        print(type(_status))
        if form.update_confirm_post.data and request.method == 'POST':
            _post_title = form.post_title.data
            session['input_post_title'] = _post_title
            _post_description = form.post_description.data
            session['input_post_description'] = _post_description
            no_title_error = None
            long_title_error = None
            no_des_error = None
            cannot_insert = False
            if not _post_title:
                no_title_error = 'Title is required.'
                cannot_insert = True
            if len(_post_title) > 255:
                long_title_error = 'Title must be less than 255 letters.'
                cannot_insert = True
            if not _post_description:
                no_des_error = 'Description is required.'
                cannot_insert = True
            if cannot_insert:
                return render_template('post_update_page.html',
                                       no_title_error=no_title_error,
                                       long_title_error=long_title_error,
                                       no_des_error=no_des_error,
                                       form=postForm(),
                                       current_name=current_name,
                                       current_id=current_id,
                                       current_type=current_type)
            return render_template('show_update_post.html',
                                   _post_title=_post_title,
                                   _post_description=_post_description,
                                   form=form,
                                   current_name=current_name,
                                   current_type=current_type,
                                   current_id=current_id)
        elif (request.method == 'POST' and form.update_clear_post.data):
            form.post_title.data = ''
            form.post_description.data = ''
            return render_template('post_update_page.html', form=form,
                                   current_id=current_id,
                                   current_name=current_name)
        if request.method == 'POST' and form.update_create_post.data:
            print('You pressed Create Btn,!')
            _post_title = session.get('input_post_title')
            _post_description = session.get('input_post_description')
            _post_status = request.form.get('options')
            _status = _post_status
            _updated_user_id = session.get('id')
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d")
            _updated_at = current_time
            sql = "UPDATE post_table SET id=%s, title=%s, description=%s, status=%s,\
                updated_user_id=%s, updated_at=%s WHERE id=%s"
            data = (id, _post_title, _post_description, _status,
                    _updated_user_id, _updated_at, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Post updated successfully!')
            resp.status_code = 200
            return redirect('/posts')
        print('You reahed here')
        return render_template('post_update_page.html', _title=_title,
                               _description=_description,
                               _status=_status,
                               current_name=current_name,
                               current_id=current_id,
                               current_type=current_type,
                               form=form)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete_post/<int:id>')
def delete_post(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM post_table WHERE id=%s", (id))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return redirect('/posts')
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


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
