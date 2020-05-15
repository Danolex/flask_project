from flask import Flask, render_template, redirect, make_response, request, session, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_login import LoginManager, login_user, logout_user, login_required
from data import db_session, __all_models, users, tables


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    email = StringField('Эл. почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_check = PasswordField('Повторите пароль', validators=[DataRequired()])
    email = StringField("Эл. почта", validators=[Email()])
    submit = SubmitField('Зарегестрироваться')


class TableForm(FlaskForm):
    add_to_cart = SubmitField('Добавить в корзину')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


@app.route('/')
@app.route('/catalog')
def catalog():
    session = db_session.create_session()
    tables_list = session.query(tables.Table)
    return render_template('catalog.html', title='Каталог', tables=tables_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Вход', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_check.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.username.data,
            email=form.email.data,
            is_admin=False
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/cart')
def cart():
    session = db_session.create_session()
    user_list = session.query(users.User).filter()
    return render_template('cart.html', title='Корзина')


@app.route('/profile')
def profile():
    return render_template('profile.html', title='Личный кабинет')


@app.route('/<type>/<style>')
def table(type, style):
    current_table = None
    session = db_session.create_session()
    table_list = session.query(tables.Table)
    s1 = int(style[0])
    s2 = int(style[-1])
    variations = []
    for el in table_list:
        if el.type == type and el.deck == s1 and el.legs == s2:
            current_table = el
        if el.type == type:
            variations.append(el)
    form = TableForm()
    if form.validate_on_submit():
        session = db_session.create_session()
    return render_template('table.html', title=type, table=current_table, form=form, vars=variations)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


db_session.global_init("db/project.sqlite")


def main():
    app.run()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
