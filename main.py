import json
import random
from flask import Flask, jsonify, render_template, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from generating_preference import GET_FRUIT_DATA
from flask_bcrypt import Bcrypt

from send_alerts import send_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hakjskjsk'  # Change this to a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

# DB Models

#user model 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.Text, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    weight = db.Column(db.Text, nullable=True)
    height = db.Column(db.Text, nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    health_history = db.Column(db.Text, nullable=True)
    fruit_preference = db.Column(db.Text, nullable=True)
    age = db.Column(db.Text, nullable=True)
    wizard_done = db.Column(db.Boolean, default=False)
    user_streak = db.Column(db.Integer, nullable=True,default=0)
    fav_fruits = db.Column(db.Text, nullable=True,default='')
    # Add more fields here!


# # User data profile
# class UserProfile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Fruit data model
class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    vitamin_c = db.Column(db.String(100), nullable=True)
    fat_content = db.Column(db.String(100), nullable=True)
    protein = db.Column(db.String(100), nullable=True)
    calories = db.Column(db.String(100), nullable=True)
    not_good_for = db.Column(db.String(100), nullable=True)
    consume_in_moderation = db.Column(db.String(100), nullable=True)
    preservation_method = db.Column(db.Text, nullable=True)
    precautions_on_overdose = db.Column(db.Text, nullable=True)
    medicinal_properties = db.Column(db.Text, nullable=True)
    history = db.Column(db.Text, nullable=True)
    image_link = db.Column(db.Text, nullable=True)

# Add fruits to database
# def add_fruit_to_db():
#     with open('fruit_data.json', 'r') as file:
#         fruit_data = json.load(file)

#     for fruit_name, fruit_details in fruit_data.items():
#         new_fruit = Fruit(
#             name=fruit_name,
#             image_link=fruit_details["image"],
#             vitamin_c=fruit_details["vitamin_c"],
#             fat_content=fruit_details["fat_content"],
#             protein=fruit_details["protein"],
#             not_good_for=", ".join(fruit_details["not_good_for"]),
#             preservation_method=fruit_details["preservation_method"],
#             precautions_on_overdose=fruit_details["precautions_on_overdose"],
#             medicinal_properties=", ".join(fruit_details["medicinal_properties"]),
#             history=fruit_details["origin_history"],
#         )
#         db.session.add(new_fruit)

#     db.session.commit()


# Create database tables
with app.app_context():
    db.create_all()
    # add_fruit_to_db()


def load_fruit_data(file_path):
    with open(file_path, 'r') as file:
        fruit_data = json.load(file)
    return fruit_data

# Load fruit data from JSON file
# fruits_data = load_fruit_data('fruit_data.json')
def open_quiz(file_path):
    with open(file_path, 'r') as file:
        quizzes = json.load(file)
    return quizzes



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            # flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        username = request.form.get('username')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            # Username already taken, flash an error message
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('register'))
        else:
            # Username available, create a new user
            password = request.form.get('password')
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=password,first_name=first_name,last_name=last_name,email=email)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            # flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('wizard'))

    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    preferred_fruits_str = current_user.fruit_preference
    preferred_fruits_list = preferred_fruits_str.split(',')
    preferred_fruits_data = []
    for fruit_name in preferred_fruits_list:
        fruit = Fruit.query.filter_by(name=fruit_name.strip()).first()
        if fruit:
            fruit_data = {
                'name': fruit.name,
                'image_link': fruit.image_link,
                'vitamin_c': fruit.vitamin_c,
                'fat_content': fruit.fat_content,
                'protein': fruit.protein,
                'preservation_method': fruit.preservation_method,
                'medicinal_properties': fruit.medicinal_properties.split(','),
                'history': fruit.history,
            }
            preferred_fruits_data.append(fruit_data)
    print(preferred_fruits_data) 
    random.shuffle(preferred_fruits_data) 
    return render_template('dashboard.html', preferred_fruits_data=preferred_fruits_data)


@app.route('/wizard', methods=['GET', 'POST'])
@login_required
def wizard():
    if current_user.wizard_done:
        return redirect(url_for('dashboard'))
    to_email = current_user.email
    subject = f"Welcome to VitaGuide! {current_user.first_name}"
    message = f"Hello {current_user.first_name}! Welcome to VitaGuide. We are glad to have you here. We hope you enjoy your stay with us."
    send_email(to_email, subject, message)
    return render_template('healthform.html',current_user=current_user)


# User data activities
@app.route('/myhealth', methods=['GET', 'POST'])
@login_required
def myhealth():
    return render_template('myhealth.html',current_user=current_user)

@app.route('/mynutrition', methods=['GET', 'POST'])
@login_required
def mynutrition():
    if current_user.fav_fruits is not None:
        favs = current_user.fav_fruits
        favorite_fruits_list = [fruit.strip() for fruit in favs.split(',') if fruit.strip()]
        fruits_data = load_fruit_data('fruit_data.json')
        return render_template('mynutrition.html',current_user=current_user, favorite_fruits_list=favorite_fruits_list,fruits_data=fruits_data)

    return render_template('mynutrition.html',current_user=current_user)

@app.route('/tracking', methods=['GET', 'POST'])
@login_required
def tracking():
    return render_template('tracking.html',current_user=current_user)

@app.route('/quizzes', methods=['GET', 'POST'])
@login_required
def quizzes():
    return render_template('quiz.html',current_user=current_user)


@app.route('/quiz/<quiz_name>')
@login_required
def show_quiz(quiz_name):

    quizzes = open_quiz('quizzes.json')
    if quiz_name in quizzes:
        return render_template('quizlet.html', questions=quizzes[quiz_name],quiz_name=quiz_name)
    else:
        return "Quiz not found"

@app.route('/submit_quiz/<quiz_name>', methods=['POST', 'GET'])
@login_required
def submit_quiz(quiz_name):
    quizzes = open_quiz('quizzes.json')
    if quiz_name in quizzes:
        score = 0
        user_answers = request.form.to_dict()

        for question in quizzes[quiz_name]: 
            question_id = str(question['id'])
            if user_answers.get(question_id) == question['correct_option']:
                score += 1
        flash(f'Your score for {quiz_name} is: {score} out of {len(quizzes[quiz_name])}', 'success')
        return render_template('score.html')
    else:
        return "Quiz not found"
 

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html',current_user=current_user)


@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def test():
    return render_template('test_preference.html',current_user=current_user)

@app.route('/setPreferences', methods=['GET', 'POST'])
@login_required
def setPref():
    user_data = request.json.get('userData', {})

    user_preferences = user_data.get('likes', []).split(",")
    allergies = user_data.get('allergies', []).split(",")
    age = user_data.get('age', [])
    gender = user_data.get('gender', [])
    country = user_data.get('country', [])
    print(user_preferences)
    print(allergies)
    # Print the received data (for testing purposes)
    # print('Received data:', user_data, allergies, user_preferences, country, gender, age)

# Save recommended fruits and allergies to the user's database record
    user = User.query.get(current_user.id)
    if user:
        recommended_fruits = GET_FRUIT_DATA(user_data)
        user.fruit_preference = ','.join(recommended_fruits)
        user.allergies = ','.join(allergies)
        user.gender = gender
        user.age = age
        user.nationality = country
        user.wizard_done = True

        # Commit changes to the database
        db.session.commit()
    return render_template('test_preference.html', current_user=current_user)



@app.route('/add-to-favorites', methods=['POST'])
@login_required  # Ensure the user is logged in
def add_to_favorites():
    fruit_name = request.form.get('fruit_name')
    if current_user.fav_fruits is None:
        current_user.fav_fruits = ''

    # Append to the existing list
    current_user.fav_fruits += ',' + fruit_name
    db.session.commit()
    flash(f'{fruit_name} add to favorites', 'success')
    return jsonify({'message': f'Added {fruit_name} to favorites!'})

@app.route('/remove-from-favorites/<string:fruit_name>', methods=['GET', 'POST'])
@login_required
def remove_from_favorites(fruit_name):
    if fruit_name in current_user.fav_fruits.split(','):
        # Remove fruit from favorites
        current_user.fav_fruits = ','.join(
            name for name in current_user.fav_fruits.split(',') if name != fruit_name
        )
        flash(f'{fruit_name} removed from favorites', 'success')
        db.session.commit()

    return redirect(url_for('mynutrition'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)

