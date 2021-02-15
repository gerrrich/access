from flask import render_template
from flask_login import LoginManager, current_user

from app import app
from app.database import Teacher, Admin, Student, db

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к системе"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    if Teacher.query.get(user_id) is not None:
        return Teacher.query.get(user_id)
    elif Student.query.get(user_id) is not None:
        return Teacher.query.get(user_id)
    else:
        return Admin.query.get(user_id)


@app.route('/home')
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.accountType == 0:
            return render_template("index.html", log='Выйти')

        elif current_user.accountType == 1:  # Student
            return render_template("index.html", log='Выйти')

        else:
            return render_template("teacher.html", log='Выйти')
    else:
        return render_template("index.html", content="Авторизуйтесь пожалуйста", log='Войти')

#
# @app.route('/login', methods=["POST", "GET"])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('logout'))
#
#     if request.method == "POST":
#         for acc in User.query.all():
#             if acc.accountLogin == request.form['accLogin'] and check_password_hash(acc.accountPassword,
#                                                                                     request.form['accPassword']):
#                 rm = True if request.form.get('remainMe') else False
#                 login_user(User().create(acc), remember=rm)
#                 return redirect(url_for('index'))
#         flash("Неверная пара логин/пароль", "error")
#     return render_template("login.html", log='Войти')
#
#
# @app.route('/logout', methods=["POST", "GET"])
# def logout():
#     if not current_user.is_authenticated:
#         return redirect(url_for('login'))
#
#     if request.method == "POST":
#         logout_user()
#         flash("Выход выполнен", "success")
#         return redirect(url_for('login'))
#     return render_template('logout.html', log='Выйти')
#
#
# @app.route('/start_work', methods=["POST", "GET"])
# def start_work():
#     if current_user.is_authenticated and current_user.accountType == 2:
#         subjects = current_user.subjects
#         if request.method == "POST":
#             key = ''
#             for i in range(6):
#                 key += str(random.choice(range(10)))
#             key_hash = generate_password_hash(key)
#             try:
#                 work = Work(key=key_hash, subject=subjects[int(request.form['subjects'])].id,
#                             type_work=bool(int(request.form['type'])), how_work=bool(int(request.form['how'])),
#                             topic=request.form['topic'], late_time=request.form['late_time'])
#                 # db.session.add(work)
#                 # db.session.flush()
#                 # db.session.commit()
#                 print('ok')
#                 return redirect(url_for('teacher_table'))
#             except:
#                 print('problem')
#         else:
#             sub = []
#             for i in range(len(subjects)):
#                 sub.append((subjects[i].name, i))
#             return render_template('start_work.html', log='Выйти', subjects=sub)
#     return redirect(url_for('login'))


# @app.route('/teacher_table')
# def teacher_table():
#    if current_user.is_authenticated and current_user.accountType == 2:
#        if current_user
#            return render_template('teacher_table.html', log='Выйти', work_key=)
#        else:
#            return redirect(url_for('start_work'))
#    return redirect(url_for('login'))
