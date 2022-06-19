
from flask import Flask, render_template,request,redirect, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.secret_key="secret"
bcrypt = Bcrypt(app)

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'juncture'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password_input = request.form['password']
        cursor = mysql.connection.cursor()
        
        query = "Select *from user_login WHERE User_Name=%s "
        cursor.execute(query,(username,))
        user = cursor.fetchone()
        print('user in db: ',user)
        if user and bcrypt.check_password_hash(user[1],password_input):
            return render_template('home.html',loggedIn = True ,username=username)
        else:
            return 'password incorrect'
        
    return render_template('login.html')

@app.route('/reset',methods=['GET','POST'])
def reset():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        new_password = request.form['new_password']
        hashed_pass = bcrypt.generate_password_hash(new_password).decode('utf-8')
        #user = {'username':username,'password':hashed_pass}
        cursor = mysql.connection.cursor()
        query1 = "Select *from user_login WHERE User_Name=%s "
        cursor.execute(query1,(username,))
        user = cursor.fetchone()
    
        if user and bcrypt.check_password_hash(user[1],password):
            print('password ', hashed_pass)
            
            query = "UPDATE user_login SET User_Password = %s"
            cursor.execute(query,(hashed_pass,))
            mysql.connection.commit()
            cursor.close()
            return render_template('home.html',loggedIn = True,reset=True)
        else:
            return 'Please enter correct password'

       
        return redirect(url_for('home'))
        
    return render_template('Register.html')

if __name__ == "__main__":
    app.run(debug=True)