from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Cấu hình đường dẫn cơ sở của ứng dụng
# base_dir là đường dẫn đến thư mục chứa app.py
basedir = os.path.abspath(os.path.dirname(__file__))

# Tạo một thể hiện (instance) của ứng dụng Flask
app = Flask(__name__)

# Cấu hình URI cho cơ sở dữ liệu SQLite
# 'sqlite:///' + đường_dẫn_tới_file_database
# File database sẽ được tạo trong thư mục gốc của dự án (my_flask_app/app.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

# Tắt tính năng theo dõi thay đổi của SQLAlchemy (tiết kiệm bộ nhớ)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Tạo đối tượng SQLAlchemy, liên kết với ứng dụng Flask
db = SQLAlchemy(app)

# ==============================================================================
# ĐỊNH NGHĨA MODEL DATABASE (Đại diện cho bảng 'post' trong cơ sở dữ liệu)
# ==============================================================================
class Post(db.Model):
    # Định nghĩa các cột của bảng
    id = db.Column(db.Integer, primary_key=True) # Cột ID, khóa chính, tự động tăng
    title = db.Column(db.String(100), nullable=False) # Cột tiêu đề, chuỗi tối đa 100 ký tự, không được rỗng
    content = db.Column(db.Text, nullable=False) # Cột nội dung, kiểu văn bản lớn, không được rỗng

    # Hàm __repr__ giúp hiển thị đối tượng Post một cách dễ đọc khi in ra console
    def __repr__(self):
        return f'<Post {self.title}>'

# ==============================================================================
# CÁC ROUTE CỦA ỨNG DỤNG
# ==============================================================================

# Route cho trang chủ - Hiển thị tất cả bài viết
@app.route('/')
def index():
    # Truy vấn tất cả các bài viết từ bảng Post
    posts = Post.query.all()
    # Truyền danh sách bài viết vào template index.html
    return render_template('index.html', posts=posts)

# Route để thêm bài viết mới
# Hỗ trợ cả phương thức GET (hiển thị form) và POST (nhận dữ liệu từ form)
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        # Lấy dữ liệu từ form khi người dùng gửi POST request
        title = request.form['title']
        content = request.form['content']

        # Tạo một đối tượng Post mới với dữ liệu nhận được
        new_post = Post(title=title, content=content)

        # Thêm đối tượng mới vào session của database
        db.session.add(new_post)
        # Lưu thay đổi vào database
        db.session.commit()

        # Chuyển hướng người dùng về trang chủ sau khi thêm bài viết thành công
        return redirect(url_for('index'))
    
    # Nếu là GET request, hiển thị form thêm bài viết
    return render_template('add_post.html')

# ==============================================================================
# KHỞI ĐỘNG ỨNG DỤNG
# ==============================================================================
if __name__ == '__main__':
    # Context ứng dụng cần thiết để thao tác với database (ví dụ: tạo bảng)
    with app.app_context():
        # Tạo tất cả các bảng trong database dựa trên các Model đã định nghĩa.
        # Dòng này chỉ cần chạy MỘT LẦN DUY NHẤT khi bạn khởi tạo database
        # Hoặc mỗi khi bạn định nghĩa model mới và muốn tạo bảng cho nó.
        # Nếu đã có database, nó sẽ không làm gì cả.
        db.create_all()
    
    # Chạy ứng dụng Flask server
    app.run(debug=True, host='0.0.0.0')