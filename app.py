from flask import Flask
from urllib.parse import quote_plus
from app.controllers.user_controller import app
from app.model.user import db

apps = Flask(__name__)

# Tách ra mật khẩu, tên người dùng, và địa chỉ localhost
db_user = 'root'
db_password = 'chinh@2003'
db_host = 'localhost'
db_name = 'diemdanhkhuonmat'

# Sử dụng pymysql
encoded_password = quote_plus(db_password)
apps.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{encoded_password}@{db_host}/{db_name}'
apps.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
apps.register_blueprint(app)

db.init_app(apps)

if __name__ == '__main__':
    with apps.app_context():
        db.create_all()
    apps.run(debug=True)
