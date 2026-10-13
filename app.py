from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from datetime import date

app = Flask(__name__)

# Create database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(350), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date)

with app.app_context():
    db.create_all()


@app.get("/")
def index():
    return render_template("index.html")

if __name__ == ("__main__"):
    app.run(debug=True)
