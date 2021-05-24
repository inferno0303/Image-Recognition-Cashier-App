from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

# 基类
db = SQLAlchemy()


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR)
    password = db.Column(db.VARCHAR)
    email = db.Column(db.VARCHAR)
    phone_number = db.Column(db.VARCHAR)
    last_login = db.Column(db.DateTime)
    sensor_count = db.Column(db.Integer)
    keys = ['id', 'username', 'password', 'email', 'phone_number', 'last_login', 'sensor_count']

    def __repr__(self):
        return '<ORM repr> (%s, %s, %s, %s)' % (self.id, self.username, self.password, self.email)


class price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.VARCHAR)
    good_name = db.Column(db.VARCHAR)
    price = db.Column(db.Integer)
    count = db.Column(db.Integer)
    other_name = db.Column(db.VARCHAR)

    def __repr__(self):
        return '<ORM repr> (%s, %s, %s, %s)' % (self.id, self.brand, self.good_name, self.price)

