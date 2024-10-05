# Module Imports
import mariadb
import pandas as pd

# Đọc dữ liệu JSON
df = pd.read_json('D:\hust\maria_db\products.json')

# Kết nối đến MariaDB trên cổng 3307
try:
    conn = mariadb.connect(
        host="127.0.0.1",  # Địa chỉ IP của máy chủ (localhost)
        user="root",  # Người dùng MariaDB (root)
        password="naq113469",  # Mật khẩu của bạn
        database="company_db",  # Tên cơ sở dữ liệu
        port=3307  # Cổng mà bạn sử dụng (3307)
    )
except mariadb.Error as e:
    print(f"Lỗi kết nối tới MariaDB: {e}")
    sys.exit(1)

# Tạo con trỏ để thực hiện các câu lệnh SQL
cursor = conn.cursor()

# Ghi dữ liệu vào bảng products
for index, row in df.iterrows():
    try:
        cursor.execute("INSERT INTO products (product_name, price, stock) VALUES (?, ?, ?)", 
                       (row['product_name'], row['price'], row['stock']))
    except mariadb.Error as e:
        print(f"Lỗi khi chèn dữ liệu: {e}")

# Lưu thay đổi và đóng kết nối
conn.commit()
cursor.close()
conn.close()

print("Đã chèn dữ liệu thành công và đóng kết nối!")
