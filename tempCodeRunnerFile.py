import mariadb
import pandas as pd
import sys

# Đọc dữ liệu từ file Excel
df = pd.read_excel('D:/hust/maria_db/orders.xlsx')

# Chuyển đổi cột 'order_date' sang định dạng datetime
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')  # 'coerce' để xử lý các giá trị không hợp lệ

# Kết nối đến MariaDB trên cổng 3307
try:
    conn = mariadb.connect(
        host="127.0.0.1",  # Địa chỉ IP của máy chủ
        user="root",  # Người dùng MariaDB
        password="naq113469",  # Mật khẩu của bạn
        database="company_db",  # Tên cơ sở dữ liệu
        port=3307  # Cổng MariaDB
    )
    print("Kết nối thành công đến MariaDB")
except mariadb.Error as e:
    print(f"Lỗi kết nối tới MariaDB: {e}")
    sys.exit(1)

# Tạo con trỏ để thực hiện các câu lệnh SQL
cursor = conn.cursor()

# Ghi dữ liệu vào bảng orders
for index, row in df.iterrows():
    try:
        # Chuyển đổi order_date sang định dạng chuỗi nếu cần
        order_date = row['order_date'].strftime('%Y-%m-%d') if pd.notnull(row['order_date']) else None

        # Thực hiện lệnh INSERT
        cursor.execute("""
            INSERT INTO orders (customer_id, product_id, quantity, order_date) 
            VALUES (%s, %s, %s, %s)
        """, (row['customer_id'], row['product_id'], row['quantity'], order_date))

        # Hiển thị thông báo sau khi chèn thành công từng bản ghi
        print(f"Đã chèn thành công dòng {index + 1} vào bảng 'orders'.")
        
    except mariadb.Error as e:
        print(f"Lỗi khi chèn dữ liệu tại dòng {index + 1}: {e}")

# Cam kết thay đổi
conn.commit()

# Đóng con trỏ và kết nối
cursor.close()
conn.close()

print("Hoàn thành quá trình nhập dữ liệu.")
