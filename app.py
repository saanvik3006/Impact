from flask import Flask, render_template, request, redirect, session
from models import db, Event, User
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.first():
        user = User(name="Student A")
        db.session.add(user)
        db.session.commit()

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']
        new_event = Event(title=title, date=date, description=description)
        db.session.add(new_event)
        db.session.commit()
        return redirect('/')
    return render_template('add_event.html')

@app.route('/register/<int:event_id>')
def register(event_id):
    user = User.query.first()
    event = Event.query.get(event_id)
    user.registered_events.append(event)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    user = User.query.first()
    return render_template('dashboard.html', events=user.registered_events)
