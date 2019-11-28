from flask import Flask, render_template, url_for, flash, redirect,request, send_file
from forms import *
import os
import mysql.connector
from plotter import obtain_plots

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

HOST = "localhost"
USER = "rhino"
PASSWORD = "iamaboy3801"
DATABASE = "uttar_pradesh"


@app.route("/")
@app.route("/home")
def home():
    connection = mysql.connector.connect(host=HOST,
    user=USER,  
    passwd=PASSWORD,
    database=DATABASE)
    cursor = connection.cursor(buffered = True)
    cursor.execute("SELECT * FROM GENERATORS ORDER BY provided DESC LIMIT 1")
    top=cursor.fetchone()
    cursor.execute("SELECT * from GENERATORS ORDER BY provided ASC LIMIT 1")
    bottom=cursor.fetchone()
    return render_template('home.html',title='Home Page',top=top,bottom=bottom)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/solar" ,methods=['GET','POST'])
def solar():
    connection = mysql.connector.connect(host=HOST,
    user=USER,  
    passwd=PASSWORD,
    database=DATABASE)
    cursor = connection.cursor(buffered = True)
    cursor.execute("SELECT * FROM solar_farm")
    farm=cursor.fetchall()
    cursor.execute("SELECT * FROM SOLAR_PROVIDER")
    prov=cursor.fetchall()
    return render_template('solar.html', title='Our Solar Energy', farm=farm , prov=prov)

@app.route("/head", methods=['GET','POST'])
def head():
    return render_template('head.html', title='IT Head')





@app.route("/mainlogin", methods=['GET','POST'])
def mainlogin():

    return render_template('mainlogin.html', title='Login')

@app.route("/hlogin", methods=['GET','POST'])
def hlogin():
    form = HeadLoginForm()
    if form.validate_on_submit():
        connection = mysql.connector.connect( host=HOST,
                                              user=USER,
                                              passwd=PASSWORD,
                                              database=DATABASE)

        cursor = connection.cursor(buffered = True)
        h_email=form.hemail.data
        h_pwd = form.hpassword.data
        cursor.execute("SELECT password FROM hlogin WHERE email_id =%s",(h_email,))
        pwdcheck=cursor.fetchone()
        if pwdcheck[0] == h_pwd :
            flash('You have been logged in!', 'success')
            return redirect(url_for('head'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('hlogin.html', title='Login', form=form)




@app.route("/register",methods=['GET','POST'])
def register():
    form1 = RegisterForm()
    if form1.validate_on_submit():
        connection = mysql.connector.connect( host=HOST,
        user=USER,
        passwd=PASSWORD,
        database=DATABASE)
        cursor = connection.cursor(buffered = True)

        aname=form1.aname.data
        amail=form1.amail.data
        pwd=form1.pwd.data

        cursor.execute("SELECT count(a_id) FROM logincheck")
        x=cursor.fetchone()

        acount=x[0]
        count1=26/(acount) 
        count2=26-int(((acount)*count1))



        #add new admin to table administrators
        cursor.execute("INSERT INTO administrators VALUES (%s,%s,%s,'2019','gen')",(acount+1,aname,count2,))
        #add new admin credentails to logincheck
        cursor.execute("INSERT INTO logincheck VALUES (%s,%s,%s)",(acount+1,amail,pwd))
        #update generator admin handling details for previously existing admins
        cursor.execute("UPDATE administrators SET num_gens=%s WHERE a_id<%s",(count1,acount+1,))
        #update admin id for each generator and genmin2
        k=1
        for i in range(int(26-count2)): #0 to 23
            cursor.execute("UPDATE GENERATORS set a_id=%s where GEN_ID=%s",(k%(acount+1)  ,(i+1),)) #circular mod add
            cursor.execute("UPDATE genmins set a_id=%s where sno=%s",(k%(acount+1)  ,(i+1),)) #updation in genmin
            if(k!=acount):
               k=k+1
            else:
               k=1
        for j in range(int(count2)): #0 to 1
            cursor.execute("UPDATE GENERATORS set a_id=%s where GEN_ID=%s",(acount+1,(26-count2+j+1),))
            cursor.execute("UPDATE genmins set a_id=%s where sno=%s",(acount+1 ,(26-count2+j+1),)) #updation in genmin



        connection.commit()
        flash('New Admin has been Registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register New Admin', form=form1)





@app.route("/login", methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        connection = mysql.connector.connect( host=HOST,
        user=USER,  
        passwd=PASSWORD,
        database=DATABASE)
        cursor = connection.cursor(buffered = True)

        a_email=form.email.data
        a_pwd = form.password.data

        cursor.execute("SELECT * FROM logincheck WHERE email_id=%s",(a_email,))
        exists=cursor.fetchone()
        if exists==None:
            flash('Admin with entered e-mail ID does not exist', 'danger')
            return redirect(url_for('login'))

        cursor.execute("SELECT password FROM logincheck WHERE email_id =%s",(a_email,))
        pwdcheck=cursor.fetchone()
        cursor.execute("SELECT a_id from logincheck WHERE email_id=%s",(a_email,))
        x=cursor.fetchone()
        aid=x[0]
            
        if pwdcheck[0] == a_pwd :
            flash('You have been logged in!', 'success')
            return redirect(url_for('admin',aid=aid))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/admin/<aid>",methods=['GET','POST'])
def admin(aid):

    connection = mysql.connector.connect( host=HOST,
    user=USER,  
    passwd=PASSWORD,
    database=DATABASE)
    cursor = connection.cursor(buffered = True)  

    cursor.execute("SELECT * FROM administrators WHERE a_id=%s",(aid,))
    y=cursor.fetchone()
    aname=y[1]
    start=y[3]
    num=y[2]
    current = 2019
    birth = y[-1]
    age = current - birth
    cursor.execute("SELECT * FROM GENERATORS WHERE a_id=%s",(aid,))
    data=cursor.fetchall()
    cursor.execute("UPDATE GENERATORS SET age=%s WHERE a_id=%s", (age,aid,))
    connection.commit()
    return render_template('admin.html',title='Admin',data=data,aid=aid,aname=aname,start=start,num=num,age=age)


@app.route("/get_plot/<gen_name>/<aid>", methods = ['GET','POST'])
def get_plot(gen_name,aid):
    bytes_obj = obtain_plots(gen_name)
    send_file(bytes_obj, 
                    attachment_filename = 'plot.png',
                    mimetype = 'image/png')
    return redirect(url_for('admin', aid=aid))


@app.route("/change/<aid>",methods=['GET','POST'])
def change(aid):
    form = ChangePasswordForm()
    if form.validate_on_submit():
      connection = mysql.connector.connect( host=HOST,
      user=USER,  
      passwd=PASSWORD,
      database=DATABASE)
      cursor = connection.cursor(buffered = True)  
      pwd=form.pwd.data
      cursor.execute("UPDATE logincheck SET password=%s WHERE a_id=%s",(pwd,aid,))     
      connection.commit()   
      flash('Password Successfully Changed!', 'success')
      return redirect(url_for('admin',aid=aid))
    return render_template('changepwd.html',title='Change Password',form=form)




if __name__ == '__main__':  
    app.run(debug=True)
