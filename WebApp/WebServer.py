
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,BeaconEvent)
import mysql.connector
from email.mime import image
from xmlrpc.client import Boolean
from flask import Flask,jsonify
import sqlite3
from flask_login import LoginManager,login_required,UserMixin,logout_user,current_user,login_user
from flask_sqlalchemy import SQLAlchemy#ORM
from werkzeug.security import generate_password_hash,check_password_hash
from line_notify import LineNotify
from flask import Flask, render_template
from flask import Flask, request, jsonify

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'AAAASSS'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SpecialProject.db'
hostname ="pe1.h.filess.io"
username ="SpecialProject_oppositeme"
password ="932f64019c479c829cf62d7abf5f19ea8a40c3ab"
database ="SpecialProject_oppositeme"
port = "3307"

line_bot_api = LineBotApi('KwOqh2ygwm/ZEELgTi8wcHx1ZTOnjkddJA1rzjBKRan7OezkRaJtstVGsgTYgtjD2KijQCS6aGsea7ivdDyQ+GX2uvE+pjqubAyokDi3VtPyN3KgFTmIFySsPMDiiKOmshW43V8evvJHx/ZWAw/j2wdB04t89/1O/w1cDnyilFU=')#YOUR_CHANNEL_ACCESS_TOKEN
handler = WebhookHandler('60b52a19ff41f94dde3df82e39789686')#YOUR_CHANNEL_SECRET
ACCESS_TOKEN = "5wMagAFZfVvwNzkqTNgZ5iD7j3pAEOdEkB81FtUFW1i"

notify = LineNotify(ACCESS_TOKEN)

class User(UserMixin,db.Model): 
    id = db.Column(db.Integer,unique=True,primary_key=True)
    username = db.Column(db.String(15),unique=True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(80))
    sensor_id = db.Column(db.String(80))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/signup', methods=['POST'])
def signup():
    # รับข้อมูลจากฟอร์ม
    email = request.form.get('user_email')
    username = request.form.get('user_name')
    password = request.form.get('user_pass')
    hashed_password = generate_password_hash(password,method='sha256')
    try:
        db.session.execute('SELECT 1')
        message = 'Connection to the database was successful!'
    except Exception as e:
        message = f'Error connecting to the database: {str(e)}'

    new_user = User(username=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()

    response_data = {
        'status': 'success',
        'message': 'User registered successfully!',
        'data': {
            'email': email,
            'username': username,
            'password': password,
            'message': message,
            'hashed_password': hashed_password,
        }
    }

    return jsonify(response_data)

@app.route('/login', methods=['POST'])
def Login():
    Username = request.form.get('user_login')
    password = request.form.get('user_pass')

    user = User.query.filter_by(username=Username).first()
    email = User.query.filter_by(email=Username).first()
    if user:    
        #print(user[1],user[2],user[3])
        print(user.id)
        if check_password_hash(user.password,password):
            login_user(user,False)
            notify.send("LoginSuccessfully")
            return render_template('Dashboard.html')
    if email:
        #print(user[1],user[2],user[3])
        print(email.id)
        if check_password_hash(email.password,password):
            login_user(email,False)
            notify.send("LoginSuccessfully")
            return jsonify({"message":True,"email":email.email,"Userid":email.id})

    return jsonify({"message":"False"})

@app.route("/Register/<Username>/<Password>/<Email>")
def InsertUser(Username,Password,Email):
    hashed_password = generate_password_hash(Password,method='sha256')
    # mydb = mysql.connector.connect(host=hostname,database=database,user=username,password=password,port=port)

    # mycursor = mydb.cursor()

    # sql = "INSERT INTO user(username,email,password) VALUES (%s,%s,%s)"
    # val = (Username,Email,hashed_password)
    # mycursor.execute(sql, val)
    # mydb.commit()

    with sqlite3.connect("SpecialProject.db") as con:
        curr = con.cursor()
        sql_cmd = """
        INSERT INTO user(username,email,password) VALUES(?,?,?);
        """
        curr.execute(sql_cmd,(Username,Email,hashed_password))
        con.commit()
    return "Hello"

# @app.route("/Login/<Username>/<password>")
# def Login(Username,password):
#     user = User.query.filter_by(username=Username).first()
#     if user:
#         #print(user[1],user[2],user[3])
#         print(user.id)
#         if check_password_hash(user.password,password):
#             login_user(user,False)
#             notify.send("LoginSuccessfully")
#             return jsonify({"message":True,"Username":user.username,"Userid":user.id})

#     return jsonify({"message":"False"})

@app.route("/")
def home():
    try:
        return render_template('Login_Page/login.html')
    except Exception as e:
        return f"An error occurred: {str(e)}"


# @app.route("/webhook",methods=['GET','POST'])
# def webhook():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     return 'OK'
    

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text="Chatนี้สำหรับการแจ้งเตือนเหตุเท่านั้น"))




# @handler.add(BeaconEvent)
# def handle_beacon(event):
#     line_bot_api.broadcast(TextSendMessage(text='found at office room 2nd floor'))
    
#     # line_bot_api.reply_message(
#     #     event.reply_token,
#     #     TextSendMessage(
#     #         text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
#     #             event.beacon.hwid, event.beacon.dm)))

if __name__ == "__main__":
    app.run(debug=True)