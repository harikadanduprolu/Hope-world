import json
import os
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
import csv  
from flask_sqlalchemy import SQLAlchemy
import sqlite3


import xlsxwriter

app = Flask(__name__)

app.static_folder = 'static'
excel_file_path = "C:\\Users\\niece\\OneDrive\\Desktop\\dt\\data..xlsx"



# Create an empty Excel writer object (if the file doesn't exist)
try:
    writer = pd.ExcelWriter(excel_file_path)
except FileNotFoundError:
    writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')  # Handle potential engine issue

try:
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
except sqlite3.OperationalError as e:
    print(f"Error connecting to database: {e}")
    exit(1)

flag=0
name=str()
class LocationForm(FlaskForm):
   location = StringField('Location')

def load_users():
    try:
        with open('users.json', 'r') as file:
            users_data = json.load(file)
            return users_data['users']
    except FileNotFoundError:
        return []

def load_queries():
    try:
        with open('queries.json', 'r') as json_file:
            queries = json.load(json_file)
            return queries
    except FileNotFoundError:
        print("JSON file 'queries.json' not found.")
        return []
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return []

def save_users(users):
    data = {'users': users}
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def opening():
    print(flag)
    return render_template('lalal.html',flag=flag)

@app.route('/lalal.html', methods=['GET'])
def lalal():
    selected_section = request.args.get('section')
    print(flag)
    return render_template('lalal.html', selected_section=selected_section,flag=flag)


@app.route('/about', methods=['GET','POST'])
def about():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args.get('name')
    print(name)
    return render_template('about.html', name=name)

@app.route('/about2', methods=['GET','POST'])
def about2():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args.get('name')
    print(name)
    return render_template('about2.html', name=name)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('opening.html')
@app.route('/home2', methods=['GET', 'POST'])
def home2():
    return render_template('home.html')

@app.route('/signup_submit', methods=['POST'])
def signup_submit():
    name = request.form['name']
    phone_number = request.form['phone_number']
    email = request.form['email']
    password = request.form['password']
    passw = request.form['passw']
    
    if passw == password:
        users = load_users()

        new_user = {'name': name, 'phone_number': phone_number, 'email': email, 'password': password}
        users.append(new_user)

        save_users(users)

        return render_template('login.html')
    
    return render_template('login.html')

@app.route('/login_submit', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']

    users = load_users()
    query_list = load_queries()

    for user in users:
        if user['email'] == username and user['password'] == password:
            global flag
            flag=flag+1
            return render_template('lalal.html', name=user['name'], queries=query_list,flag=flag)
    
    return jsonify({'message': 'Login failed. Please check your username and password.'})

@app.route('/form1')
def form1():
    return render_template('form1.html')

@app.route('/submit_form1', methods=['POST'])
def submit_form1():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form.get('age', '')  # Consider validation for numeric type
        gender = request.form['gender']
        place = request.form['place']

        # Handle additional fields
        phone = request.form.get('phone', '')
        relation = request.form.get('relation', '')
        ngoName = request.form.get('ngoName', '')

        data = {
            'name': name,
            'age': age,
            'gender': gender,
            'place': place,
            'phone': phone,
            'relation': relation,
            'ngoName': ngoName
        }
        df = pd.DataFrame([data])

        try:
            # Create a new file if it doesn't exist, otherwise append to existing file
            mode = 'w' if not os.path.exists(excel_file_path) else 'a'
            with pd.ExcelWriter(excel_file_path, mode=mode, engine='openpyxl') as writer:
                # If it's a new file, add header, otherwise omit
                header = False if mode == 'a' else True
                df.to_excel(writer, sheet_name='formData', index=False, header=header)
            return 'Form submitted successfully'
        except Exception as e:  # Catch broader exceptions
            print(f"Error writing to Excel file: {e}")
            return render_template('form2.html')



def submit_form():
    if request.method == 'POST':
        form_type = request.form['formType']
        if form_type == 'your':
            name = request.form['name']
            age = request.form['age']
            gender = request.form['gender']
            place = request.form['place']
        elif form_type == 'friend':
            name = request.form['name']
            age = request.form['age']
            gender = request.form['gender']
            place = request.form['place']
            phone = request.form.get('phone', '')
            c.execute("INSERT INTO formData (name, age, gender, place, phone) VALUES (?, ?, ?, ?, ?)",
                      (name, age, gender, place, phone))
            conn.commit()
            return 'Form submitted successfully'
        elif form_type == 'relative':
            name = request.form['name']
            relation = request.form['relation']
            age = request.form['age']
            place = request.form['place']
            phone = request.form.get('phone', '')
        elif form_type == 'ngo':
            name_org = request.form['ngoName']
            cause = request.form['cause']
            place = request.form['place']
        elif form_type == 'other':
            age = request.form['age']
            gender = request.form['gender']
            place = request.form['place']
            phone = request.form.get('phone', '')
        conn.commit()
        
        return 'Form submitted successfully'

@app.route('/found', methods=['POST'])
def found():
    query_list = load_queries()
    return render_template('found.html',queries=query_list)

if __name__ == '__main__':
    app.run(debug=True)
