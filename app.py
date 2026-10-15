from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import date, datetime

app = Flask(__name__)

# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my-secret-key'

db = SQLAlchemy(app)

CATEGORY_LABELS = {
    "Food": "Ăn uống",
    "Transport": "Di chuyển",
    "Rent": "Tiền nhà",
    "Utilities": "Điện nước",
}


@app.context_processor
def inject_category_labels():
    # Biến này dùng được trong mọi template
    return {"category_labels": CATEGORY_LABELS}


class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(350), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)


with app.app_context():
    db.create_all()


# Return home page
@app.get("/")
def index():
    expenses = Expenses.query.order_by(Expenses.date.desc(), Expenses.id.desc()).all()

    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=['POST'])
def add():
    # Get Data
    description = (request.form.get("description") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    if not description or not amount_str or not category:
        flash("Vui lòng điền thông tin mô tả, số tiền và danh mục.", "error")
        return redirect(url_for("index"))

    # Chỉ nhận danh mục có trong bảng
    if category not in CATEGORY_LABELS:
        flash("Danh mục không hợp lệ.", "error")
        return redirect(url_for("index"))

    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Số tiền phải là số dương.", "error")
        return redirect(url_for("index"))

    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        d = date.today()

    # Save data
    e = Expenses(description=description, amount=amount, category=category, date=d)

    db.session.add(e)
    db.session.commit()

    flash("Đã thêm khoản chi.", "success")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)