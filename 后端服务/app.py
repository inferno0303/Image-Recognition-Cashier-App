# author: LSY
# version: 20190528

from flask import *
from ConfigReader import *
from mysql_orm import *


app = Flask(__name__)

# 初始化MySQL
MYSQL_CONFIG = get_mysql_config()
MYSQL_USER = MYSQL_CONFIG['MYSQL_USER']
MYSQL_PASSWORD = MYSQL_CONFIG['MYSQL_PASSWORD']
MYSQL_HOST = MYSQL_CONFIG['MYSQL_HOST']
MYSQL_DB = MYSQL_CONFIG['MYSQL_DB']
MYSQL_URI = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_HOST + '/' + MYSQL_DB
app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_ECHO"] = False
db.init_app(app)

# TODO 首页
@app.route('/')
def index_page():
    return send_file('pages/login/login.html')

# TODO 登录页模块
from pages.login.login import login
app.register_blueprint(login, url_prefix='/login')

# TODO 主页模块
from pages.home.home import home
app.register_blueprint(home, url_prefix='/home')

# TODO 测试模块
from pages.service.service import service
app.register_blueprint(service, url_prefix='/service')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)
