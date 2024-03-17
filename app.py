from flask import Flask,render_template,url_for,redirect,request
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
session = db.session
#.....model....#
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contactNumber = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)


class Owner(db.Model):
    __tablename__ = 'Owner'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

@app.route('/home')
def index():
    user= User.query.all()
    return render_template('index.html',users=user)

# ...

@app.route('/<int:user_id>/')
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    print("create method called")
    if request.method == 'POST':
        print("post method called")
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        contactNumber = request.form['contactNumber']
        city = request.form['city']
        # age = int(request.form['age'])
        print("value fetched")
        user = User(email = email, contactNumber =  contactNumber, city = city, firstName = firstname, lastName = lastname)
        print("user created")
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('Create.html')



@app.route('/home/update/<int:user_id>/', methods=('GET', 'POST'))
def update(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        print("current user is", user)
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        contactNumber = request.form['contactnumber']
        city = request.form['city']
        print("all good")
        user.firstName = firstname
        user.lastName = lastname
        user.email = email
        user.contactNumber = contactNumber
        user.city = city
        print("user after updating value is", user)
        try:
            db.session.commit()
        except Exception as e:
            print("some error occured")
        return redirect(url_for('index'))
    return render_template('update.html', user=user)
# ...

@app.post('/home/delete/<int:user_id>/')
def delete(user_id):
    print("delete called ")
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        owner = db.session.query(Owner).filter((Owner.email == email) & (Owner.password  == password))
        ln = len(owner.all())
        if ln == 1:
            return redirect((url_for('index')))
        else:
            print("login failed")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # global owner
            owner = Owner(email=email, password=password)
            # self.owner = own
            session.add(owner)
            session.commit()
            print("User added successfully!")
        except Exception as e:
            # global owner
            print("Error adding user:", e)
            session.rollback()
            return redirect(url_for('register'))
            # TODO show error page
        return redirect(url_for('index'))
    return render_template('register.html')

with app.app_context():
    db.create_all()

if __name__ == "__main__":

    app.run(debug=True)
