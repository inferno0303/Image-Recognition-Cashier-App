from mysql_orm import *
from common_lib import *
from flask import *
home = Blueprint('home', __name__)


def db_get_user_infos(username):
    username = str(username)
    data = db.session.query(user).filter(user.username == username).limit(1).values(user.username, user.password, user.email, user.phone_number, user.last_login, user.sensor_count)
    data = [i for i in data][0]
    ret = {'username': data.username, 'password': data.password, 'email': data.email, 'phone_number': data.phone_number, 'last_login': str(data.last_login), 'sensor_count': data.sensor_count}
    return ret


# TODO home首页
@home.route('/')
def render_home_page():
    return send_file('pages/home/home.html')


# TODO 用户信息
@home.route('/get_user_infos')
def get_user_infos():
    try:
        user_cookie = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookie)
        if username:
            ret = db_get_user_infos(username)
            print(ret)
            return api_resp(code=0, msg=ret)
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()


@home.route('/get_all_price')
def get_all_price():
    try:
        user_cookie = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookie)
        if username:
            db_ret = db_get_all_price()
            return api_resp(code=0, msg=db_ret)
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()


def db_get_all_price():
    db_ret = db.session.query(price).all()
    print(db_ret)
    ret = []
    for i in db_ret:
        ret.append({'id': i.id, 'brand': i.brand, 'good_name': i.good_name, 'price': i.price, 'count': i.count, 'other_name': i.other_name})
    return ret


@home.route('/submit_modi_price', methods=['POST'])
def submit_modi_price():
    try:
        user_cookie = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookie)
        if username:
            id = request.form['id']
            brand = request.form['brand']
            good_name = request.form['good_name']
            price = request.form['price']
            count = request.form['count']
            other_name = request.form['other_name']
            ret = db_submit_modi_price({'id': id, 'brand': brand, 'good_name': good_name, 'price': price, 'count': count, 'other_name': other_name})
            db_ret = 'ok'
            return api_resp(code=0, msg=db_ret)
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_err_resp(msg=e)


def db_submit_modi_price(info):
    db_rec = db.session.query(price).filter(price.id == info['id']).first()
    db_rec.brand = info['brand']
    db_rec.good_name = info['good_name']
    db_rec.price = info['price']
    db_rec.count = info['count']
    db_rec.other_name = info['other_name']
    db.session.commit()
    return 'ok'
