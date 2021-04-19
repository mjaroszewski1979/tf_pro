from flask import Flask,render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import pandas_datareader.data as pdr
import datetime
import flask_login
import threading
from send_mail import send_mail
from get_trend import get_trend, markets, markets_pro, data, data_pro
from models import Markets, MarketsPro







app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stocks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

logins = {'name': {'password': 'password'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(name):
    if name not in logins:
        return

    user = User()
    user.id = name
    return user


@login_manager.request_loader
def request_loader(request):
    name = request.form.get('name')
    if name not in logins:
        return

    user = User()
    user.id = name

    user.is_authenticated = request.form['password'] == logins[name]['password']

    return user


@app.route('/')
def index_get():
    all_markets = Markets.query.order_by(Markets.name).all()
    return render_template('index.html',all_markets=all_markets,  data=[{'name':'S&P 500'}, {'name':'GOLD'}, {'name':'BITCOIN'}] )

@app.route('/pro')
@flask_login.login_required
def pro_get():
    all_markets = MarketsPro.query.order_by(MarketsPro.name).all()
    return render_template('pro.html',all_markets=all_markets,  data_pro=[{'name':'S&P 500'}, {'name':'NASDAQ'}, {'name':'DOW JONES'}, {'name':'NIKKEI'}, {'name':'GOLD'}, {'name':'SILVER'}, {'name':'BITCOIN'}, {'name':'LITECOIN'}, {'name':'ETHEREUM'}, {'name':'US DOLLAR'}, {'name':'JP YEN'}, {'name':'CH FRANC'}, {'name':'CA DOLLAR'}] )

@app.route('/', methods=['POST'])
def index_post():
    err_msg = ''
    new_market = request.form.get('market')
    if new_market:
        existing_market = Markets.query.filter_by(name=new_market).first()
        if not existing_market:
            symbol = markets[new_market]
            new_trend = get_trend(symbol)
            data = Markets(name=new_market, symbol=symbol, trend=new_trend)
            db.session.add(data)
            db.session.commit()
        else:
            err_msg = 'MARKET ALREADY ADDED. BECOME A PRO MEMBER AND GET ACCESS TO MORE FINANCIAL INSTRUMENTS!'

    if err_msg:
        flash(err_msg)
    else:
        flash('MARKET ADDED. BECOME A PRO MEMBER AND GET ACCESS TO MORE FINANCIAL INSTRUMENTS!')
    return redirect(url_for('index_get'))

@app.route('/pro', methods=['POST'])
@flask_login.login_required
def pro_post():
    err_msg = ''
    new_market = request.form.get('market')
    if new_market:
        existing_market = MarketsPro.query.filter_by(name=new_market).first()
        if not existing_market:
            symbol = markets_pro[new_market]
            new_trend = get_trend(symbol)
            data = MarketsPro(name=new_market, symbol=symbol, trend=new_trend)
            db.session.add(data)
            db.session.commit()
        else:
            err_msg = 'MARKET ALREADY ADDED'

    if err_msg:
        flash(err_msg)
    else:
        flash('MARKET ADDED')
    return redirect(url_for('pro_get'))



@app.route('/delete/<int:id>')
def delete(id):
    market = Markets.query.get_or_404(id)
    db.session.delete(market)
    db.session.commit()
    return redirect(url_for('index_get'))

@app.route('/delete_pro/<int:id>')
@flask_login.login_required
def delete_pro(id):
    market = MarketsPro.query.get_or_404(id)
    db.session.delete(market)
    db.session.commit()
    return redirect(url_for('pro_get'))

@app.route('/update/<int:id>')
def update(id):
    market = Markets.query.get_or_404(id)
    symbol = market.symbol
    new_trend = get_trend(symbol)
    market.trend = new_trend
    db.session.commit()
    return redirect(url_for('index_get'))

@app.route('/update_pro/<int:id>')
@flask_login.login_required
def update_pro(id):
    market = MarketsPro.query.get_or_404(id)
    symbol = market.symbol
    new_trend = get_trend(symbol)
    market.trend = new_trend
    db.session.commit()
    return redirect(url_for('pro_get'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    try:
        name = request.form['name']
        if request.form['password'] == data[name]['password']:
            user = User()
            user.id = name
            flask_login.login_user(user)
            return redirect(url_for('pro_get'))
        flash('WRONG NAME OR PASSWORD!')
        return redirect(url_for('login'))
    except KeyError:
        flash('WRONG NAME OR PASSWORD!')
        return redirect(url_for('login'))



@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return render_template('logout.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        t1 = threading.Thread(target=send_mail, args=[name, email])
        t1.start()
        flash('THANK YOU. PLEASE CHECK YOUR EMAIL!')
        return redirect(url_for('login'))
    return render_template('register.html')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('unauthorized.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

    
if __name__ == '__main__':
    app.run()
