import sqlite3
connection = sqlite3.connect("cinema.db")
cursor = connection.cursor()

#cursor.execute(""" CREATE TABLE IF NOT EXISTS bookings (
#booking_id INTEGER NOT NULL PRIMARY KEY, movie TEXT, seats INTEGER, amount REAL)""")

# cursor.execute("""
# INSERT INTO bookings (movie, seats, amount)
# VALUES ('Solar Drift', 2, 700)
# """)
#
# cursor.execute("""
# INSERT INTO bookings (movie, seats, amount)
# VALUES ('Midnight Code', 4, 1200)
# """)

# connection.commit()
#
# cursor.execute("SELECT * FROM bookings")
# print(cursor.fetchall())


import pandas as pd
df=pd.read_sql_query("select * from bookings",connection)
print(df)