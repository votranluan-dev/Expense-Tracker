from flask import Flask, Response, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import date, datetime

from sqlalchemy import func

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
    "Health": "Sức khỏe",
}

def parse_date_or_none(s: str):
    if not s:
        return None 
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:  
        return None


@app.context_processor
def inject_category_labels():
    return {"category_labels": CATEGORY_LABELS}


class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(350), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)


with app.app_context():
    db.create_all()

@app.template_filter("vnd")
def vnd(value):
    return f"{value or 0:,.0f}".replace(",", ".")



# Return home page
@app.get("/")
def index():
    # Filter expenses 
    # 1. Read query str
    start_str = (request.args.get("start") or "").strip() 
    end_str = (request.args.get("end") or "").strip()
    selected_category = (request.args.get("category") or "").strip()

    # 2. Pasing
    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    if start_date and end_date and end_date < start_date:
        flash("Ngày kết thúc phải sau ngày bắt đầu.", "error")
        start_date = None
        start_str = ""

    q = Expenses.query
    
    if start_date:
        q = q.filter(Expenses.date >= start_date)
    if end_date:
        q = q.filter(Expenses.date <= end_date)

    if selected_category:
        q = q.filter(Expenses.category == selected_category)

    # Get all expenses and total amount
    expenses = q.order_by(Expenses.date.desc(), Expenses.id.desc()).all()

    total = round(sum(e.amount for e in expenses), 2)

    # Pie Chart
    cat_q = db.session.query(Expenses.category, func.sum(Expenses.amount))

    if start_date:
        cat_q = cat_q.filter(Expenses.date >= start_date)
    if end_date:
        cat_q = cat_q.filter(Expenses.date <= end_date)
    if selected_category:
        cat_q = cat_q.filter(Expenses.category == selected_category)

    cat_row = cat_q.group_by(Expenses.category).all()
    cat_labels = [CATEGORY_LABELS.get(c, c) for c, _ in cat_row]
    cat_values = [round(float(s or 0), 2) for _, s in cat_row]

    # Day Chart
    day_q = db.session.query(Expenses.date, func.sum(Expenses.amount))

    if start_date:
        day_q = day_q.filter(Expenses.date >= start_date)
    if end_date:
        day_q = day_q.filter(Expenses.date <= end_date)
    if selected_category:
        day_q = day_q.filter(Expenses.category == selected_category)

    day_row = day_q.group_by(Expenses.date).order_by(Expenses.date).all()
    day_labels = [d.strftime("%Y-%m-%d") for d, _ in day_row]
    day_values = [round(float(s or 0), 2) for _, s in day_row]
    

    return render_template(
        "index.html", 
        expenses=expenses,
        total=total,
        start_str=start_str,
        end_str=end_str,
        today=date.today().strftime("%Y-%m-%d"),
        selected_category=selected_category,
        cat_labels=cat_labels,
        cat_values=cat_values,
        day_labels=day_labels,
        day_values=day_values
    )



@app.route("/add", methods=['POST'])
def add():
    # Get Data
    description = (request.form.get("description") or "").strip()
    amount_str = (request.form.get("amount") or "").strip().replace(".", "")
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


@app.route("/delete/<int:id>", methods=['POST'])
def delete(id):
    e = Expenses.query.get_or_404(id)

    db.session.delete(e)
    db.session.commit()

    flash("Đã xóa khoản chi.", "success")

    return redirect(url_for("index"))


@app.route("/export.csv")
def export_csv():
    # 1. Read query str
    start_str = (request.args.get("start") or "").strip() 
    end_str = (request.args.get("end") or "").strip()
    selected_category = (request.args.get("category") or "").strip()

    # 2. Pasing
    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    q = Expenses.query
    
    if start_date:
        q = q.filter(Expenses.date >= start_date)
    if end_date:
        q = q.filter(Expenses.date <= end_date)
    if selected_category:
        q = q.filter(Expenses.category == selected_category)

    expenses = q.order_by(Expenses.date.desc(), Expenses.id).all()

    lines = ["Ngày, Mô tả, Danh mục, Số tiền"]

    for e in expenses:
        lines.append(f"{e.date}, {e.description}, {CATEGORY_LABELS.get(e.category, e.category)}, {e.amount}")

    csv_data = "\n".join(lines)

    fname_start = start_str or "all"
    fname_end = end_str or "all"
    filename = f"expenses_{fname_start}_{fname_end}.csv"

    return Response (
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "COntent-Type": "text/csv; charset=utf-8"
        }
    )


if __name__ == "__main__":
    app.run(debug=True)