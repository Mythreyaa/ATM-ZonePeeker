from flask import Flask, render_template, request
from templates.compare import *
from splay import *
import csv
import cx_Oracle

try:
    con =  cx_Oracle.connect('scott/tiger@localhost:1521/orclab')
    cursor = con.cursor()
    print(cursor,"------------------------------!!!!----------------------------------------")
except:
    print("Error in connecting with Oracle Database")

app = Flask(__name__)
app.debug = True
splay = SplayTrees()

def drop():
    drop = "DROP TABLE USER_INFO"
    cursor.execute(drop)

def create():
    global cursor
    print(cursor,"hi")
    create = "CREATE TABLE USER_INFO(User_ID VARCHAR(50) PRIMARY KEY,UFName VARCHAR(50),ULName VARCHAR(50),UPwd VARCHAR(50))"
    cursor.execute(create)
    print("!!!!!!CREATED!!!!!!!")

def insert(list):
    cursor.execute("INSERT INTO USER_INFO (User_ID, UFName, ULName, UPwd) VALUES (:1,:2,:3,:4)",list)
    con.commit()
    
    show()

def show():
    show = "SELECT * FROM USER_INFO"
    cursor.execute(show)
    row = cursor.fetchall()
        
    for user in row:
        print(user)
        print("\n")
    print("\n")

def user_info(id,pwd):
    print(id,pwd)
    info = "SELECT User_ID,UFName,ULName,UPwd FROM USER_INFO WHERE User_ID = :id AND UPwd = :pwd"
    cursor.execute(info,id=id,pwd=pwd)
    row = cursor.fetchall()

    if row != []:
        return True
    else:
        return False

@app.route('/')
def signuphome():
    try:
        create()
    except:
        print("Already created")
    return render_template('signup.html')

@app.route('/process-form', methods=['GET','POST'])
def signup_form():
    fname = request.form.get('FName')
    lname = request.form.get('LName')
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    cpwd = request.form.get('cpwd')
    
    print([fname,lname,email,pwd])
    insert([email,fname,lname,pwd])
    # with open('users.csv','a') as csvfile: 
    #     csvwriter = csv.writer(csvfile) 
    #     csvwriter.writerow([fname,lname,email,pwd])
    return render_template('Header.html')

@app.route('/signin')
def signinhome():
    return render_template('signin.html')

@app.route('/signin/process-form', methods=['GET','POST'])
def signin_form():
    print("hi")
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    
    print(email,pwd)
    if user_info(email,pwd):
        return render_template('Header.html')
    return render_template('signin.html')
    # with open("users.csv","r") as f:
    #     reader = csv.reader(f)
    #     for i in reader :
    #         if i == [] :
    #             continue
    #         elif i[2] == email and i[-1] == pwd :
    #             return render_template('Header.html')
    
    
@app.route("/signin/process-form/home")
def header():
    return render_template('Header.html')

@app.route("/signup/process-form/getyourlocation")
def get_your_location():
    return render_template('getlocation.html')

@app.route("/signup/process-form/getyourlocation", methods=['GET','POST'])
def get_your_location_form():
    bankname = request.form.get("bankname")
    bankaddress = request.form.get("bankaddress")
    pref_location1 = request.form.get("location1")
    pref_location2 = request.form.get("location2")
    pref_location3 = request.form.get("location3")
    population_density = request.form.get("Population density")
    radius = request.form.get("Radius")
    
    print(bankname,bankaddress,pref_location1,pref_location2,pref_location3,population_density,radius)
    print("-----------------------------------------------")

    search = splay.search([(bankname,bankaddress),
                     (pref_location1,pref_location2,pref_location3)])
    if search:
        print("From splay")
        print(search)
        return render_template('display.html',pri_locations = search[2],user = search[0])
    
    pri_list = find_loc(bankname,bankaddress,pref_location1,pref_location2,pref_location3,population_density,radius)
    # print(pri_list)

    splay.insert([(bankname,bankaddress),(pref_location1,pref_location2,pref_location3),pri_list])
    return render_template('display.html',pri_locations = pri_list,user = (bankname,bankaddress))

@app.route("/contact")
def contact():
    return render_template('contactus.html')


if __name__ == '__main__':
    app.run()

        


