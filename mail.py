import json
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.static_folder = 'static'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poverty_areas.db'
db = SQLAlchemy(app)

class PovertyArea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pincode = db.Column(db.String(10))
    area = db.Column(db.String(100))

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
    name = 'na/'
    return render_template('opening.html', name=name)

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
            return render_template('home.html', name=user['name'], queries=query_list)
    
    return jsonify({'message': 'Login failed. Please check your username and password.'})

@app.route('/create', methods=['GET', 'POST'])
def create_query():
    return render_template('query.html')

@app.route('/other', methods=['POST'])
def other():
    return render_template('other.html')

@app.route('/employment', methods=['POST'])
def employment():
    return render_template('employment.html')

@app.route('/education', methods=['POST'])
def education():
    return render_template('education.html')

@app.route('/housing', methods=['POST'])
def housing():
    return render_template('housing.html')

@app.route('/health', methods=['POST'])
def health():
    return render_template('health.html')

@app.route('/food', methods=['POST'])
def food():
    return render_template('food.html')

@app.route('/near', methods=['POST'])
def near():
    return render_template('near.html')

@app.route('/par', methods=['POST'])
def par():
    return render_template('par.html')

@app.route('/submit', methods=['POST'])
def submit():
    pincode = int(request.form['pincode'])  
    nearest_areas = [str(i) for i in range(pincode, pincode + 50)]
    return render_template('areas.html', areas=nearest_areas)

if __name__ == '__main__':
    app.run(debug=True)
