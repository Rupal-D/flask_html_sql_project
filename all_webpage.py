from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_cors import cross_origin
import pandas as pd
import pyodbc
database={'Akshara':'172401','Bopanna':'172402','Nishmitha':'172403','Dhanashree':'172404','Krithi':'172405','Mohammed':'172406','Manjunath':'172407','Nithin':'172408','Pooja':'172409','Sushma':'172410'}

#connection to database
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=LAPTOP-9S9AO7N8;'
                      'Database=Webpage;'
                      'Trusted_Connection=yes;');
app = Flask(__name__)
app.secret_key = 'Bye' 


@app.route("/")             #This is a decorator.
@cross_origin()
def home():
    return render_template("index.html")


@app.route('/LOGIN', methods=['POST','GET']) 
@cross_origin()
def login():
    flag = 0
    if request.method == 'POST':
        user = request.form['name']   #'name' is the name in the dictionary key.
        pwd = request.form['password']
        for key, value in database.items():
            if key == user and value == pwd:
                session['user'] = user      #'user' is the name of the dictionary key.
                #flash("Login Succesful!")
                return redirect(url_for("insert"))
                flag = 1
                break
        if flag == 0:
            flash("INCORRECT USERNAME or PASSWORD !!")
            return redirect(url_for('login'))
    else:
        if 'user' in session:       #Check notes 446-448.
            flash("Already logged in")
            return redirect(url_for('insert'))

        return render_template('login.html')

@app.route('/user')
@cross_origin()
def user():
    if 'user' in session:
        user = session['user']
        return render_template('user.html', user = user)
    else:
        flash("You are not logged in yet.")
        return redirect(url_for('login'))

@app.route('/logout')
@cross_origin()
def logout():
    #The next 3 lines of code is for checking if the user is in the session. And if he is there then we will logout with the user name.
    if 'user' in session:
        user = session['user']
        flash(f"You have succesfully logged out, {user}.","info")
    session.pop('user',None)    #Remove the user data from our sessions. None is a message associated with removing that data.
    return redirect(url_for('home'))


@app.route("/Student", methods = ["GET", "POST"])
@cross_origin()
def Student():
    data1 = pd.read_sql("SELECT * FROM Student", conn)
    result1=data1.to_html()
    return result1

@app.route("/Courses", methods = ["GET", "POST"])
@cross_origin()
def Courses():
    data2 = pd.read_sql("SELECT * FROM Courses", conn)
    result2=data2.to_html()
    return result2

@app.route("/subjects", methods = ["GET", "POST"])
@cross_origin()
def subjects():
    data3 = pd.read_sql("SELECT * FROM subjects", conn)
    result3=data3.to_html()
    return result3

@app.route("/exams", methods = ["GET", "POST"])
@cross_origin()
def exams():
    data4 = pd.read_sql("SELECT * FROM exams", conn)
    result4=data4.to_html()
    return result4

@app.route("/grade_card", methods = ["GET", "POST"])
@cross_origin()
def grade_card():
    data5 = pd.read_sql("SELECT * FROM grade_card", conn)
    result5=data5.to_html()
    return result5

@app.route("/Faculty", methods = ["GET", "POST"])
@cross_origin()
def Faculty():
    data6 = pd.read_sql("SELECT * FROM Faculty", conn)
    result6=data6.to_html()
    return result6


@app.route("/OVERLOOK", methods = ["GET", "POST"])
@cross_origin()
def Overlook():
    return render_template('overlook.html')

@app.route("/insert", methods=["GET","POST"])
@cross_origin()
def insert():
    if request.method ==  "POST":
        return redirect(url_for("manipulation"))
    return render_template("submit.html")


@app.route("/submit", methods = ["GET", "POST"])
@cross_origin()
def manipulation():
    option = request.form['name']
    if option == 'case1':
        s1 = request.form['Insert_S_s1']
        s2 = request.form['Insert_S_s2']
        s3 = request.form['Insert_S_s3']
        s4 = request.form['Insert_S_s4']
        s5 = request.form['Insert_S_s5']
        s6 = request.form['Insert_S_s6']
        s7 = request.form['Insert_S_s7']
        s8 = request.form['Insert_S_s8']
        s9 = request.form['Insert_S_s9']
        s10 = request.form['Insert_S_s10']
        s11 = request.form['Insert_S_s11']
        record = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11]
    
        cursor = conn.cursor()
        insert="INSERT INTO Student_manipulation values(?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(insert,record)
        manipulation = pd.read_sql("SELECT * from Student_manipulation", conn)
        result = manipulation.to_html()

    elif option == 'case2':
        s1 = request.form['Delete_S']
        cursor=conn.cursor()
        delete ="DELETE FROM Student_manipulation where sid=?"
        cursor.execute(delete ,s1)
        data = pd.read_sql("SELECT * FROM Student_manipulation", conn)
        result=data.to_html()

    elif option == 'case3':
        r1 = request.form['Update_S_r1']
        r2 = request.form['Update_S_r2']
        record=[r2,r1]
        cursor=conn.cursor()
        update="UPDATE Student_manipulation SET email_id=? WHERE sid=?"
        cursor.execute(update,record)
        data = pd.read_sql("SELECT * FROM Student_manipulation", conn)
        result=data.to_html()
    else:
        pass
    return result



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8513, debug = True) 
