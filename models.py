
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
