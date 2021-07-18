from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import re

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Vijisam@12345'
app.config['MYSQL_DB']='fooddelivery'

mysql=MySQL(app)

@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST':
        global username
        username=request.form['username']
        password=request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("select * from userdetails where Username=%s AND password=%s",(username,password,))
        data=cur.fetchone()
        if data:
            msg='Logged in successfully!'
            return render_template('order.html',msg=msg)
        else:
            msg='Incorrect username/password' 
    return render_template('login.html',msg=msg) 


@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method=='POST':
        global name 
        name=request.form['name']
        global username
        username=request.form['username']
        password=request.form['password']
        address=request.form['address']
        phnno=request.form['phnno']
        email=request.form['email']
        cur=mysql.connection.cursor()
        cur.execute("select * from userdetails where Username=%s AND password=%s",(username,password,))
        data=cur.fetchone()
        if data:
            msg='Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            mas="Invalid email address"
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg='Username must contain only characters'
        elif not len(phnno)>=10:
            msg='Phone number not valid'
        else:
            cur.execute('insert into userdetails values(NULL,%s,%s,%s,%s,%s,%s)',(name,username,password,phnno,email,address,))
            mysql.connection.commit()
            msg='You have successfully registered!'
    elif request.method=='POST':
        msg='Please fill out the form!'
    return render_template('register.html',msg=msg)



@app.route('/order',methods=['GET','POST'])
def order():
    global food
    food=request.form['food']
    count=request.form['count']
    cur=mysql.connection.cursor()
    cur.execute("select Cost from fooditems where Foodname like %s",(food,)) 
    data=cur.fetchone()
    global totalcost
    totalcost=int(count)*int(data[0])
    totalcost=str(totalcost)
    cur.execute('insert into orderdetails values(%s,%s,%s,%s)',(username,food,count,totalcost,))
    cur.execute('select Name from userdetails where Username like %s',(username,))
    data=cur.fetchone()
    global name
    name=data[0]
    cur.execute('insert into output values(%s,%s,%s)',(name,food,totalcost,))
    mysql.connection.commit()
    return redirect(url_for('success',name=name))

@app.route('/success',methods=['GET','POST'])
def success():
    data=[]
    data.append(name)
    data.append(food)
    data.append(totalcost)
    return render_template('success.html',data=data)



@app.route('/output',methods=['GET','POST'])
def output():
    cur=mysql.connection.cursor()
    cur.execute("select * from output where Name like %s",(name,))
    data=cur.fetchall()
    cur.close()
    return render_template('output.html',data=data)
        
if __name__=="__main__":
    app.run(debug=True)


