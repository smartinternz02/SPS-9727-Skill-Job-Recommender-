from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__) # to make the app run without any

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'r7HrwQRCQ6'
app.config['MYSQL_PASSWORD'] = 'hGa3HuPK6w'
app.config['MYSQL_DB'] = 'r7HrwQRCQ6'

mysql = MySQL(app)

app.secret_key = 'mysecret'

global userid

@app.route('/register',methods =['GET', 'POST'])
def registr():
    msg=''
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method =='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username, email,password))
            mysql.connection.commit()
            return render_template('welcome.html');
    elif request.method == 'POST':
        msg = 'Please fill the details to proceed!'        
        return render_template('register.html', msg= msg);
    return render_template('register.html', msg= msg);


@app.route('/login',methods =['GET', 'POST'])
def login():
    msg=''
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            return render_template('welcome.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
        
    

@app.route("/")
def start():
    return render_template('start.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True,port = 5000)