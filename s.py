from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

app = Flask(__name__)

# Tách ra mật khẩu, tên người dùng, và địa chỉ localhost
db_user = 'root'
db_password = 'chinh@2003'
db_host = 'localhost'
db_name = 'diemdanhkhuonmat'

# Sử dụng pymysql thay vì mysqlconnector
encoded_password = quote_plus(db_password)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{encoded_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f"Post('{self.title}', '{self.content}')"


@app.route('/')
def index():
    users = Users.query.all()
    return render_template('index.html', users=users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Chạy lệnh trong ngữ cảnh ứng dụng Flask
    app.run(debug=True)
