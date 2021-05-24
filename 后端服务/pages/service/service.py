from mysql_orm import *
from common_lib import *
from flask import *
service = Blueprint('service', __name__)


def db_get_user_infos(username):
    username = str(username)
    data = db.session.query(user).filter(user.username == username).limit(1).values(user.username, user.password, user.email, user.phone_number, user.last_login, user.sensor_count)
    data = [i for i in data][0]
    ret = {'username': data.username, 'password': data.password, 'email': data.email, 'phone_number': data.phone_number, 'last_login': str(data.last_login), 'sensor_count': data.sensor_count}
    return ret


# TODO home首页
@service.route('/')
def render_home_page():
    return send_file('pages/service/service.html')


@service.route('/query_price_info')
def query_price_info():
    try:
        # user_cookie = request.cookies['LOGIN_SESSION']
        # username = check_permission(cookie=user_cookie)
        if 'username':
            keyword = request.args['keyword']
            db_ret = db_query_price_info(keyword)
            if db_ret:
                return api_resp(code=0, msg=db_ret)
            else:
                return api_resp(code=1, msg='没有该商品')
        # else:
        #     pass
    except Exception as e:
        print(e)
        return api_resp_permission_error()


def db_query_price_info(keyword):
    print(keyword)
    db_ret = db.session.query(price).filter(db.or_(price.good_name.like("%" + keyword + "%"), price.other_name.like("%" + keyword + "%"))).first()
    if db_ret is not None:
        ret = {'id': db_ret.id, 'brand': db_ret.brand, 'good_name': db_ret.good_name, 'price': db_ret.price, 'count': db_ret.count,
           'other_name': db_ret.other_name}
        print(ret)
        return ret
    else:
        return None