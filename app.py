from flask import Flask, render_template, request, url_for, make_response, flash, redirect
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


@app.route("/add", methods=['POST'])
def add():
    description = (request.form.get("description") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    if not description or not amount_str or not category:
        flash("Vui lòng điền thông tin mô tả, số tiền và danh mục.", "error")
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Số tiền phải là số dương.", "error")
        return redirect(url_for("index"))


    print("From received:", dict(request.form))
    return make_response("From received check the console")

if __name__ == ("__main__"):
    app.run(debug=True)
