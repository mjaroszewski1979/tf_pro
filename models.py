class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(name):
    if name not in data:
        return

    user = User()
    user.id = name
    return user


@login_manager.request_loader
def request_loader(request):
    name = request.form.get('name')
    if name not in data:
        return

    user = User()
    user.id = name

    user.is_authenticated = request.form['password'] == data[name]['password']

    return user


class Markets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    symbol = db.Column(db.String(20))
    trend = db.Column(db.String(20))

class MarketsPro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    symbol = db.Column(db.String(20))
    trend = db.Column(db.String(20))