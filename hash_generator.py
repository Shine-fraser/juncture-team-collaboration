from flask import Flask, render_template,request,redirect, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.secret_key="secret"
bcrypt = Bcrypt(app)

password='admin'

hashed_pass = bcrypt.generate_password_hash(password).decode('utf-8')
@app.route('/')
def get_pass():
    return hashed_pass
print(hashed_pass)
if __name__ == "__main__":
    app.run(debug=True)