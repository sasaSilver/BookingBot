import sqlite3 as sq

db = sq.connect('tg.db')
cur = db.cursor()

async def db_start():
    cur.execute('CREATE TABLE IF NOT EXISTS bookings('
                'user_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'bookings_id TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS bookings('
                'booking_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'time_start TEXT'
                'time_end TEXT')
    db.commit()
