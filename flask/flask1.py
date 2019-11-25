from flask import Flask, render_template, url_for, flash, redirect,request
from forms import LoginForm,HeadLoginForm,RegisterForm,RemoveForm,ChangePasswordForm
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
    connection = mysql.connector.connect(host="localhost",
    user="root",  
    passwd="7338330380",
    database="uttar_pradesh")
    cursor = connection.cursor(buffered = True)
    cursor.execute("SELECT * from generators order by provided desc limit 1")
    top=cursor.fetchone()
    cursor.execute("SELECT * from generators order by provided asc limit 1")
    bottom=cursor.fetchone()
    print(bottom)
    return render_template('home.html',title='Home Page',top=top,bottom=bottom)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/solar" ,methods=['GET','POST'])
def solar():
    connection = mysql.connector.connect(host="localhost",
    user="root",  
    passwd="7338330380",
    database="uttar_pradesh")
    cursor = connection.cursor(buffered = True)

    cursor.execute("SELECT * FROM solar_farm")
    farm=cursor.fetchall()
    print(farm)

    cursor.execute("SELECT * FROM solar_provider")
    prov=cursor.fetchall()

    return render_template('solar.html', title='Our Solar Energy', farm=farm , prov=prov)

@app.route("/mainlogin", methods=['GET','POST'])
def mainlogin():
    
    return render_template('mainlogin.html', title='Login')

@app.route("/hlogin", methods=['GET','POST'])
def hlogin():
    form = HeadLoginForm()
    if form.validate_on_submit():
        connection = mysql.connector.connect( host="localhost",
    user="root",  
    passwd="7338330380",
    database="uttar_pradesh")
        cursor = connection.cursor(buffered = True)
        h_email=form.hemail.data
        h_pwd = form.hpassword.data
        
        print(h_email)
        #checkpwd =( "SELECT password FROM logincheck WHERE email_id ='%s'",(a_email,))
        #print(checkpwd)
        cursor.execute("SELECT password FROM hlogin WHERE email_id =%s",(h_email,))
        pwdcheck=cursor.fetchone()
        print(pwdcheck[0])

                 
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
        connection = mysql.connector.connect( host="localhost",
        user="root",  
        passwd="7338330380",
        database="uttar_pradesh")
        cursor = connection.cursor(buffered = True)
        aname=form1.aname.data
        print(aname)
        amail=form1.amail.data
        print(amail)
        pwd=form1.pwd.data


        
        cursor.execute("SELECT count(a_id) from loginchecks")
        x=cursor.fetchone()
        acount=x[0]
        print(acount) #presently existing admin count
        count1=26/(acount+1) #for the existing admins
        count2=26-((acount+1)*count1) #for the newly added admin

        
        
        #add new admin to table administrators
        cursor.execute("INSERT into admins VALUES (%s,%s,%s,'2019','gen')",(acount+1,aname,count2,))
        #add new admin credentails to logincheck
        cursor.execute("INSERT into loginchecks VALUES (%s,%s,%s)",(acount+1,pwd,amail,))
        #update generator admin handling details for previously existing admins
        cursor.execute("UPDATE admins set num_gens=%s where a_id<%s",(count1,acount+1,))

        #update admin id for each generator and genmin2
        k=1 
        for i in range(26-count2): #0 to 23
            cursor.execute("UPDATE generators set a_id=%s where GEN_ID=%s",(k%(acount+1)  ,(i+1),)) #circular mod add
            cursor.execute("UPDATE genmins set a_id=%s where sno=%s",(k%(acount+1)  ,(i+1),)) #updation in genmin
            if(k!=acount):
               k=k+1
            else:
               k=1
       
        for j in range(count2): #0 to 1
            cursor.execute("UPDATE generators set a_id=%s where GEN_ID=%s",(acount+1,(26-count2+j+1),)) 
            cursor.execute("UPDATE genmins set a_id=%s where sno=%s",(acount+1 ,(26-count2+j+1),)) #updation in genmin
            

               
        connection.commit()
        flash('New Admin has been Registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register New Admin', form=form1)



@app.route("/head", methods=['GET','POST'])
def head():
    return render_template('head.html', title='IT Head')

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
        
        print(a_email)
        #checkpwd =( "SELECT password FROM logincheck WHERE email_id ='%s'",(a_email,))
        #print(checkpwd)
        cursor.execute("SELECT * from loginchecks where email_id=%s",(a_email,))
        exists=cursor.fetchone()
        if exists==None:
            flash('Admin with entered e-mail ID does not exist', 'danger')
            return redirect(url_for('login'))
        cursor.execute("SELECT password FROM loginchecks WHERE email_id =%s",(a_email,))
        pwdcheck=cursor.fetchone()
        print(pwdcheck[0])

        cursor.execute("SELECT a_id from loginchecks WHERE email_id=%s",(a_email,))
        x=cursor.fetchone()
        aid=x[0]
        print(aid)
       # out = [item for t in pwdcheck for item in t] 
       # print(out)

         
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
    passwd="7338330380",
    database="uttar_pradesh")
    cursor = connection.cursor(buffered = True)  
    print(aid)
    cursor.execute("SELECT * from admins WHERE a_id=%s",(aid,))
    y=cursor.fetchone()
    aname=y[1]
    start=y[3]
    num=y[2]


    print(aname)
    cursor.execute("SELECT * FROM generators WHERE a_id=%s",(aid,))
    data=cursor.fetchall()
    print(data)

    return render_template('admin.html',title='Admin',data=data,aid=aid,aname=aname,start=start,num=num)

if __name__ == '__main__':  
    app.run(debug=True)

@app.route("/change/<aid>",methods=['GET','POST'])
def change(aid):
    form = ChangePasswordForm()
    if form.validate_on_submit():
      connection = mysql.connector.connect( host="localhost",
      user="root",  
      passwd="7338330380",
      database="uttar_pradesh")
      cursor = connection.cursor(buffered = True)  
      print(aid)
      pwd=form.pwd.data
      cursor.execute("UPDATE loginchecks set password=%s WHERE a_id=%s",(pwd,aid,))     
   
      connection.commit()   
      flash('Password Successfully Changed!', 'success')
      return redirect(url_for('admin',aid=aid))
    return render_template('changepwd.html',title='Change Password',form=form)
if __name__ == '__main__':  
    app.run(debug=True)


    '''@app.route("/remove",methods=['GET','POST'])
def remove():
    form1 = RemoveForm()
    if form1.validate_on_submit():
        connection = mysql.connector.connect( host="localhost",
        user="root",  
        passwd="7338330380",
        database="uttar_pradesh")
        cursor = connection.cursor(buffered = True)
        aid=form1.aid.data
        print(aid)
                
        cursor.execute("SELECT count(a_id) from logincheck")
        x=cursor.fetchone()
        acount=x[0]
        print(acount)
        count1=26/(acount) #for n-1 admins
        count2=26-((acount-1)*count1) #for the nth admin

        #delete admin credentails from logincheck
        cursor.execute("DELETE from logincheck where a_id=%s",(aid,))

        
        #update admin id for each generator and genmin2 assuming that aids will be reassigned
        k=1
        for i in range(26-count2): #0 to 23
            cursor.execute("UPDATE generators set a_id=%s where GEN_ID=%s",(k%(acount)  ,(i+1),)) #circular mod add
            cursor.execute("UPDATE genmin2 set a_id=%s where sno=%s",(k%(acount)  ,(i+1),)) #updation in genmin
            if(k!=acount-1):
               k=k+1
            else:
               k=1
       
        for j in range(count2): #0 to 1
            cursor.execute("UPDATE generators set a_id=%s where GEN_ID=%s",(acount,(26-count2+j+1),)) 
            cursor.execute("UPDATE genmin2 set a_id=%s where sno=%s",(acount ,(26-count2+j+1),)) #updation in genmin
            
        #delete admin from table administrators
        cursor.execute("DELETE FROM administrators WHERE a_id=%s",(aid,))
        
        #update generator admin handling details for currently existing admins
        cursor.execute("UPDATE administrators set num_gens=%s where a_id<%s",(count1,acount,))
        cursor.execute("UPDATE administrators set num_gens=%s where a_id=%s",(count2,acount,))

        connection.commit()
        flash('Admin has been Removed!', 'success')
        return redirect(url_for('login'))
    return render_template('remove.html', title='Remove Admin', form=form1) '''