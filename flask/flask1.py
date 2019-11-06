from flask import Flask, render_template, url_for, flash, redirect,request
from forms import LoginForm
import os
import mysql.connector

# mydb=mysql.connector.connect(
#      host="localhost",
#     user="root",  
#     passwd="7338330380",
#     database="uttar_pradesh"
#     )
# cursor=mydb.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/login", methods=['GET','POST'])


def login():
    form = LoginForm()
    if form.validate_on_submit():
        connection = mysql.connector.connect( host="localhost",
    user="root",  
    passwd="7338330380",
    database="uttar_pradesh")
        cursor = connection.cursor(buffered = True)
        a_email=form.email.data
        a_pwd = form.password.data
        

#        x=("select * from generators where GEN_ID=3");
 #       cursor.execute(x)
  #      a=cursor.fetchall()
   #     print(a)
        print(a_email)
        #checkpwd =( "SELECT password FROM logincheck WHERE email_id ='%s'",(a_email,))
        #print(checkpwd)
        cursor.execute("SELECT password FROM logincheck WHERE email_id =%s",(a_email,))
        pwdcheck=cursor.fetchone()
        print(pwdcheck[0])
        
        cursor.execute("SELECT a_id from logincheck WHERE email_id=%s",(a_email,))
        x=cursor.fetchone()
        aid=x[0]
        print(aid)


       # out = [item for t in pwdcheck for item in t] 

       # print(out)

       # pwdcheck=""
       # for i in range(0,len(out)):
       #     pwdcheck+=out[i]
       # print(pwdcheck)
      #  print(pwdcheck.replace('(', ''))
      #  print(pwdcheck.replace(')', ''))
      #  print(pwdcheck.replace("'", ''))
      #  print(pwdcheck.replace(',', ''))
      


        if pwdcheck[0] == a_pwd :
            flash('You have been logged in!', 'success')
            return redirect(url_for('admin'),aid=aid)
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/admin/<int:aid>")
def admin(aid):
    cursor.execute("SELECT * FROM generators WHERE a_id=aid")
    data=cursor.fetchall()
    print(data)
    return render_template('admin.html',title='Admin',data=data)

if __name__ == '__main__':
    app.run(debug=True)
