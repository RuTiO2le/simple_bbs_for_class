from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.chat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Chat(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_name = db.Column(db.String(16), nullable=False)
  message = db.Column(db.String(128), nullable=False)
  timestamp = db.Column(db.String(28), nullable=False)


@app.route('/')
def index():
  data = Chat.query.all()
  return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add():
  user_name = request.form['user_name']
  message = request.form['message']
  jp_timezone = pytz.timezone('Asia/Tokyo') # 日本の標準時間を指定
  dt_now = datetime.datetime.now(jp_timezone) # デフォルトだとUTC+0になる(おそらくreplitのサーバがイギリスにある)
  timestamp = dt_now.strftime('%Y/%m/%d %H:%M:%S')
  if not (user_name):
    user_name = "名無しの人"
  new_message = Chat(message=message, user_name=user_name, timestamp=timestamp)
  db.session.add(new_message)
  db.session.commit()
  return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
