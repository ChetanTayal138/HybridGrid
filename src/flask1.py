from flask import Flask, render_template, url_for, flash, redirect,request , send_file
from forms import LoginForm
import os
import mysql.connector
from plotter import obtain_plots

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
    passwd="iamaboy3801",
    database="uttar_pradesh")
        cursor = connection.cursor(buffered = True)
        a_email=form.email.data
        a_pwd = form.password.data
        cursor.execute("SELECT password FROM logincheck WHERE email_id =%s",(a_email,))
        pwdcheck=cursor.fetchone()
        cursor.execute("SELECT a_id from logincheck WHERE email_id=%s",(a_email,))
        x=cursor.fetchone()
        aid=x[0]
        print(aid)
       
         
        if pwdcheck[0] == a_pwd :
            flash('You have been logged in!', 'success')
            return redirect(url_for('admin',aid=aid))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/admin/<aid>",methods=['GET','POST'])
def admin(aid):
    connection = mysql.connector.connect( host="localhost",
    user="root",  
    passwd="iamaboy3801",
    database="uttar_pradesh")
    cursor = connection.cursor(buffered = True)  
    cursor.execute("SELECT * from administrators WHERE a_id=%s",(aid,))
    y=cursor.fetchone()
    aname=y[1]
    start=y[3]
    num=y[2]
    cursor.execute("SELECT * FROM generators WHERE a_id=%s",(aid,))
    data=cursor.fetchall()
    

    return render_template('admin.html',title='Admin',data=data,aid=aid,aname=aname,start=start,num=num)


@app.route("/solar" ,methods=['GET','POST'])
def solar():
    connection = mysql.connector.connect(host="localhost",
    user="root",  
    passwd="iamaboy3801",
    database="uttar_pradesh")
    cursor = connection.cursor(buffered = True)

    cursor.execute("SELECT * FROM solar_farm")
    farm=cursor.fetchall()
    print(farm)

    cursor.execute("SELECT * FROM solar_provider")
    prov=cursor.fetchall()

    return render_template('solar.html', title='Our Solar Energy', farm=farm , prov=prov)


@app.route("/get_plot/<gen_name>/<aid>", methods = ['GET','POST'])

def get_plot(gen_name,aid):
    print(gen_name)
    print(aid)

    bytes_obj = obtain_plots(gen_name)
    send_file(bytes_obj, 
                    attachment_filename = 'plot.png',
                    mimetype = 'image/png')

    return redirect(url_for('admin', aid=aid))



if __name__ == '__main__':  
    app.run(debug=True)