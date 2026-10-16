# Expense Tracker – Quản lý chi tiêu
Ứng dụng web quản lý chi tiêu cá nhân viết bằng Flask, lưu dữ liệu bằng SQLite. Giao diện hoàn toàn bằng tiếng Việt, số tiền tính theo VND và hiển thị có dấu chấm ngăn cách hàng nghìn (ví dụ '1.250.000 VND').

# Tính năng
- Thêm, sửa, xóa khoản chi (mô tả, số tiền, ngày, danh mục).
- Ô nhập số tiền tự thêm dấu chấm khi gõ ('1000' → '1.000').
- Lọc danh sách theo khoảng ngày và danh mục.
- Hiển thị tổng chi tiêu theo bộ lọc hiện tại.
- Biểu đồ tròn chi tiêu theo danh mục và biểu đồ cột chi tiêu theo ngày.
- Xuất CSV theo bộ lọc hiện tại.
- Danh mục có sẵn: Ăn uống, Di chuyển, Tiền nhà, Điện nước, Sức khỏe.

# Công nghệ sử dụng
| Thành phần    | Công nghệ                             |
---------------------------------------------------------
| Backend       | Python, Flask, Flask-SQLAlchemy       |
| Cơ sở dữ liệu | SQLite (file 'instance/expenses.db')  |
| Giao diện     | Jinja2, Tailwind CSS (CDN)            |
| Biểu đồ       | Chart.js (CDN)                        |

Lưu ý: Tailwind CSS và Chart.js được tải từ CDN, nên máy cần có kết nối Internet khi mở ứng dụng. Nếu không có mạng, trang sẽ mất giao diện và biểu đồ.

# Yêu cầu
- Python 3.10 trở lên (được phát triển và chạy thử trên Python 3.15).
- pip (đi kèm Python).
- Git (nếu muốn clone project).

Kiểm tra phiên bản Python:
'''bash
python --version
'''

Trên Windows nếu lệnh 'python' không chạy, hãy thử 'py --version'. Khi cài Python, nhớ tick vào ô "Add python.exe to PATH".

# Cài đặt và chạy
1. Tải project
'''bash
git clone https://github.com/votranluan-dev/Expense-Tracker.git
cd Expense-Tracker
'''

Hoặc tải file ZIP trên GitHub, giải nén rồi mở terminal trong thư mục vừa giải nén.

2. Tạo môi trường ảo (venv)
Thư mục 'venv/' không có sẵn trong repo (đã bị ẩn bởi '.gitignore'), bạn cần tự tạo:
Windows (PowerShell):
'''powershell
python -m venv venv
venv\Scripts\Activate.ps1
'''

Nếu PowerShell báo lỗi về *execution policy*, chạy một lần lệnh sau rồi kích hoạt lại:
'''powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
'''

Windows (Command Prompt):
'''cmd
python -m venv venv
venv\Scripts\activate.bat
'''

macOS / Linux:
'''bash
python3 -m venv venv
source venv/bin/activate
'''

Kích hoạt thành công khi đầu dòng terminal có chữ '(venv)'.

3. Cài thư viện
'''bash
pip install -r requirements.txt
'''

Nếu chỉ muốn cài các thư viện chính, bạn có thể chạy 'pip install Flask Flask-SQLAlchemy', các thư viện còn lại sẽ tự được cài kèm.

4. Chạy ứng dụng
'''bash
python app.py
'''

Hoặc dùng lệnh của Flask (Flask tự nhận file 'app.py'):
'''bash
flask run --debug
'''

Mở trình duyệt và truy cập: http://127.0.0.1:5000

Lần chạy đầu tiên, ứng dụng tự tạo file cơ sở dữ liệu 'instance/expenses.db', bạn không cần làm gì thêm.

Muốn dừng server, nhấn 'Ctrl + C' trong terminal. Muốn thoát môi trường ảo, gõ 'deactivate'.

Cấu trúc thư mục
'''
Expense-Tracker/
├── app.py                 # Toàn bộ code Flask: model, route, bộ lọc
├── requirements.txt       # Danh sách thư viện (kèm phiên bản)
├── templates/
│   ├── base.html          # Khung chung: header, thông báo flash, footer
│   ├── index.html         # Trang chính: form, bộ lọc, bảng, biểu đồ
│   └── edit.html          # Trang sửa khoản chi
├── csv/                   # Một vài file CSV xuất thử
├── instance/              # (tự tạo) chứa expenses.db – bị .gitignore ẩn
├── venv/                  # (tự tạo) môi trường ảo – bị .gitignore ẩn
└── .gitignore
'''

Các route
| Phương thức   | Đường dẫn         | Chức năng                                                 |
-------------------------------------------------------------------------------------------------
| GET           | '/'               | Trang chính. Nhận tham số lọc 'start', 'end', 'category'  |
| POST          | '/add'            | Thêm khoản chi                                            |
| GET, POST     | '/edit/<id>'      | Mở form sửa (GET) và lưu thay đổi (POST)                  |
| POST          | '/delete/<id>'    | Xóa khoản chi                                             |
| GET           | '/export.csv'     | Tải CSV, nhận cùng các tham số lọc như trang chính        |

Ví dụ lọc khoản chi "Ăn uống" từ 01/10 đến 31/10/2026:

'''
http://127.0.0.1:5000/?start=2026-10-01&end=2026-10-31&category=Food
'''

# Về file '.gitignore'
Một số file và thư mục cố ý không có trong repo. Dưới đây là việc cần làm với từng mục sau khi clone:
| Mục bị ẩn | Lý do | Bạn cần làm gì |
| --- | --- | --- |
| 'venv/' | Môi trường ảo nặng và phụ thuộc từng máy | Tự tạo bằng 'python -m venv venv', rồi 'pip install -r requirements.txt' |
| 'instance/', '*.db', '*.sqlite3' | Chứa dữ liệu chi tiêu thật của người dùng | Không cần làm gì, 'expenses.db' tự được tạo khi chạy lần đầu |
| '.flaskenv' | Cấu hình biến môi trường riêng của máy | Không bắt buộc. Project chạy được bằng 'python app.py'. Nếu muốn dùng 'flask run', hãy tạo file này (xem bên dưới) |
| '.env' | Nơi để các thông tin bí mật (khóa, mật khẩu) | Hiện project chưa dùng. Nếu sau này cần thì tự tạo |
| '__pycache__/', '*.pyc' | File Python tự sinh khi chạy | Không cần làm gì |
| '.vscode/', '.DS_Store', 'Thumbs.db' | File cấu hình editor và file rác của hệ điều hành | Không cần làm gì |

## Tạo '.flaskenv' (tùy chọn)
Tạo file '.flaskenv' ở thư mục gốc với nội dung:
'''
FLASK_APP=app
FLASK_DEBUG=1
'''

Sau đó cài thêm 'pip install python-dotenv' để Flask tự đọc file này, rồi chạy 'flask run'.

# Xử lý sự cố thường gặp
'Python was not found' khi tạo venv (Windows).
Bạn chưa cài Python hoặc quên tick "Add to PATH". Thử 'py -m venv venv'. Nếu vẫn lỗi, cài lại Python từ python.org rồi mở lại terminal. Có thể tắt luôn shortcut của Microsoft Store tại *Settings → Apps → Advanced app settings → App execution aliases*.

'ModuleNotFoundError: No module named 'flask''.
Bạn chưa kích hoạt venv hoặc chưa cài thư viện. Kiểm tra đầu dòng có '(venv)' chưa, rồi chạy 'pip install -r requirements.txt'.

Trang mất giao diện hoặc biểu đồ không hiện.
Tailwind CSS và Chart.js tải từ Internet. Hãy kiểm tra kết nối mạng.

Cổng 5000 đang bị chiếm ('Address already in use').
Chạy ở cổng khác: 'flask run --port 5001', rồi mở 'http://127.0.0.1:5001'.

Muốn xóa sạch dữ liệu để bắt đầu lại.
Dừng server, xóa file 'instance/expenses.db', rồi chạy lại. Ứng dụng sẽ tạo database mới trống.

# Lưu ý bảo mật

Trong 'app.py', 'SECRET_KEY' đang để giá trị mẫu ('my-secret-key') và ứng dụng chạy ở chế độ 'debug=True'. Cấu hình này chỉ phù hợp để học tập và chạy trên máy cá nhân. Nếu đưa lên server thật, hãy đổi 'SECRET_KEY' sang chuỗi ngẫu nhiên (đọc từ biến môi trường), tắt debug và dùng một WSGI server như Gunicorn hoặc Waitress.

# Lịch sử phát triển

Project được xây dựng theo từng bước, mỗi commit là một tính năng (C1 – C13): cài đặt, cấu hình SQLite, tạo model, form thêm khoản chi, lưu vào database, hiển thị danh sách, tính tổng, xóa, lọc theo ngày, biểu đồ, xuất CSV và chỉnh sửa. Bạn có thể xem lại từng bước bằng 'git log --oneline'.
