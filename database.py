import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect("salon.db")
    c = conn.cursor()
    
    # Таблица записей
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        client_name TEXT,
        client_username TEXT,
        service TEXT,
        master TEXT,
        date TEXT,
        time TEXT,
        status TEXT DEFAULT 'pending'
    )''')
    
    conn.commit()
    conn.close()

def get_available_times(master, date):
    all_times = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
    
    conn = sqlite3.connect("salon.db")
    c = conn.cursor()
    c.execute("SELECT time FROM bookings WHERE master=? AND date=? AND status='confirmed'", (master, date))
    booked = [row[0] for row in c.fetchall()]
    conn.close()
    
    return [t for t in all_times if t not in booked]

def add_booking(client_id, client_name, client_username, service, master, date, time):
    conn = sqlite3.connect("salon.db")
    c = conn.cursor()
    c.execute('''INSERT INTO bookings 
        (client_id, client_name, client_username, service, master, date, time)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (client_id, client_name, client_username, service, master, date, time))
    booking_id = c.lastrowid
    conn.commit()
    conn.close()
    return booking_id

def confirm_booking(booking_id):
    conn = sqlite3.connect("salon.db")
    c = conn.cursor()
    c.execute("UPDATE bookings SET status='confirmed' WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()

def get_booking(booking_id):
    conn = sqlite3.connect("salon.db")
    c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE id=?", (booking_id,))
    row = c.fetchone()
    conn.close()
    return row

def get_next_7_days():
    days = []
    today = datetime.now()
    for i in range(1, 8):
        day = today + timedelta(days=i)
        if day.weekday() != 6:  # пропускаем воскресенье
            days.append(day.strftime("%d.%m.%Y"))
    return days

init_db()