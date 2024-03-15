from flask import Flask
from urllib.parse import quote_plus
from app.controllers.user_controller import user_bp
from app.model.user import db

app = Flask(__name__)

# Tách ra mật khẩu, tên người dùng, và địa chỉ localhost
db_user = 'root'
db_password = 'chinh@2003'
db_host = 'localhost'
db_name = 'diemdanhkhuonmat'

# Sử dụng pymysql
encoded_password = quote_plus(db_password)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{encoded_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(user_bp)

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
