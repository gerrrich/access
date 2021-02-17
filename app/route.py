import random, datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from app.database import Teacher, Admin, Student, db, Lesson

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к системе"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    if Teacher.query.get(user_id) is not None:
        return Teacher.query.get(user_id)
    elif Student.query.get(user_id) is not None:
        return Student.query.get(user_id)
    else:
        return Admin.query.get(user_id)


@app.route('/home')
@app.route('/')
def index():
    if current_user.is_authenticated:
        if str(current_user) == '1':  # Admin
            return render_template('index.html',
                                   content='Привет админ', log='Выйти')

        elif str(current_user) == '2':  # Student
            return render_template('index.html',
                                   content='Привет студент', log='Выйти')

        else:
            return render_template('teacher.html', log='Выйти')
    else:
        return render_template("index.html",
                               content='Авторизуйтесь пожалуйста', log='Войти')


def login_help(type):
    user = [Admin, Student, Teacher]
    for acc in user[type].query.all():
        if acc.login == request.form['login'] and \
                check_password_hash(acc.password, request.form['password']):
            rm = True if request.form.get('remainMe') else False
            login_user(user[type]().create(acc), remember=rm)
            return redirect(url_for('index'))
    return None


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('logout'))

    if request.method == "POST":
        user = login_help(0)
        if user:
            print('Teacher login')
            return user

        user = login_help(1)
        if user:
            print('Student login')
            return user

        user = login_help(2)
        if user:
            print('Admin login')
            return user

        flash("Неверная пара логин/пароль", "error")
    return render_template("login.html", log='Войти')


@app.route('/logout', methods=["POST", "GET"])
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == "POST":
        logout_user()
        flash("Выход выполнен", "success")
        return redirect(url_for('login'))
    return render_template('logout.html', log='Выйти')


def teacher_on_lesson(teacher):
    for les in Lesson.query.all():
        if les.teacher == current_user.show_id() and \
                les.date == datetime.datetime.today().date() and \
                les.end_time > datetime.datetime.today().time():
            return les
    return None


@app.route('/start_lesson', methods=["POST", "GET"])
def start_work():
    if current_user.is_authenticated and str(current_user) == '3':
        subjects = current_user.subjects
        if request.method == "POST":
            key = ''
            for i in range(6):
                key += str(random.choice(range(10)))
            try:
                lesson = Lesson(key=key,
                                subject=subjects[
                                    int(request.form['subjects'])].id,
                                teacher=current_user.show_id(),
                                type=bool(int(request.form['type'])),
                                format=bool(int(request.form['how'])),
                                topic=request.form['topic'],
                                late_time=int(request.form['late_time']),
                                start_time=datetime.datetime.today().time(),
                                end_time=(datetime.datetime.today() +
                                          datetime.timedelta(
                                              hours=1, minutes=30)).time(),
                                date=datetime.datetime.today().date())
                db.session.add(lesson)
                db.session.flush()
                db.session.commit()
                print('ok')
                return redirect(url_for('teacher_table'))
            except:
                print('problem')
        else:
            lesson = teacher_on_lesson(current_user)
            if lesson:
                return redirect(url_for('teacher_table'))
            sub = []
            for i in range(len(subjects)):
                sub.append((subjects[i].name, i))
            return render_template('start_lesson.html', log='Выйти',
                                   subjects=sub)
    return redirect(url_for('login'))


@app.route('/teacher_table')
def teacher_table():
    if current_user.is_authenticated and str(current_user) == '3':
        lesson = teacher_on_lesson(current_user)
        if lesson:
            return render_template('teacher_table.html', log='Выйти',
                                   work_key=lesson.key)
        else:
            return redirect(url_for('start_work'))
    return redirect(url_for('login'))
