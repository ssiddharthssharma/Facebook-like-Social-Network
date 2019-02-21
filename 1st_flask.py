from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f921075e726a2fd04c50a78b2d89d363'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'#/// means relative path
db= SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')	
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')" 

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	data_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)		

	def __repr__(self):
		return f"User('{self.title}', '{self.data_posted}'" 

posts = [
		{
			'author' : 'Sid',
			'title'	 : 'Post 1',
			'content': 'First post content',
			'date_posted': 'October 10, 2018'
		},
		{
			'author' : 'Pradeep',
			'title'	 : 'Post 2',
			'content': '2nd post content',
			'date_posted': 'October 12, 2018'
		},
		{
			'author' : 'Sahil',
			'title'	 : 'Post 3',
			'content': '3rd post content',
			'date_posted': 'October 14, 2018'
		},
		{
			'author' : 'Namrita',
			'title'	 : 'Post 4',
			'content': '4th post content',
			'date_posted': 'October 16, 2018'
		}

]

owner = 'Siddharth'


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title= (owner +'\'s Wall') , posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About ')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	#if form.validate_on_submit():
	return render_template('login.html', title='Login', form=form)
       

if __name__ == '__main__':
	app.run(debug=True)

