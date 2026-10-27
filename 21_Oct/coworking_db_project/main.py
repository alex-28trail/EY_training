import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="coworking_demo",
    user="postgres",
    port="5432",
    password="Admin@123"
)

cursor = conn.cursor()

print("Connected to PostgreSQL")

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS rooms (
#     room_id SERIAL PRIMARY KEY,
#     room_name VARCHAR(100),
#     capacity INT,
#     hourly_rate DECIMAL(10,2),
#     status VARCHAR(100)
# )
# """)
#
# conn.commit()
#
# print("Table created")

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS bookings (
#     bookings_id SERIAL PRIMARY KEY,
#     room_id INT REFERENCES rooms(room_id),
#     booked_by VARCHAR(100),
#     booking_date TIMESTAMP NOT NULL,
#     hours INT
# )
# """)
#
# conn.commit()
#
# print("Table 2 created")

# cursor.execute("""
# INSERT INTO rooms
# (room_id,room_name, capacity, hourly_rate ,status)
# VALUES
# (001,'Focus Room', 250, 500, 'Confirmed'),
# (002,'Conference Room', 200, 300, 'Pending'),
# (003,'Creative Studio', 500, 400, 'Pending'),
# (004,'Board Room', 30, 750, 'Confirmed')
# """)
#
# conn.commit()
#
# print("Records inserted")

cursor.execute("SELECT * FROM rooms")
rows = cursor.fetchall()
for row in rows:
    print(row)


# cursor.execute("""
# INSERT INTO bookings
# ( bookings_id, room_id, booked_by, booking_date,hours)
# VALUES
# (101,001,'Anvi', '2026-10-12', 48),
# (102,002,'Cyrus', '2026-11-23', 30),
# (103,003,'Deepak', '2026-9-28', 13),
# (104,004,'Vinil', '2026-12-25', 72)
# """)
# conn.commit()
#
# print("Records inserted")

cursor.execute("SELECT * FROM bookings")
rows = cursor.fetchall()
for row in rows:
    print(row)