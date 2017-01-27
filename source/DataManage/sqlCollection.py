import sqlite3

dbname = 'obd.db'

def create(dbname):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    try:
        cursor.execute("""CREATE TABLE row_obd (
                             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                             time DATE NOT NULL,
                             vss FLOAT NOT NULL,
                             maf FLOAT NOT NULL,
                             kpl FLOAT NOT NULL);""")

    except sqlite3.Error as e:
        print('Failed to creat table:', e)

    connection.commit()
    connection.close()

    return True

def put_data(obd_data):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    try:
        data = []
        for i in obd_data:
            data.append(i)

        cursor.execute("INSERT INTO rowOBDdata (time, vss, maf, kpl) VALUES (?, ?, ?, ?)", (data[0], data[1], data[2], data[3]))

    except sqlite3.Error as e:
        print('Failed to insert data:', e)

    connection.commit()
    connection.close()

    return True

def get_history_data(time_cond):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    try:
        results = cursor.execute("SELECT time,vss,maf,kpl FROM rowOBDdata Where time between ? and ?",(time_cond[0],time_cond[1]))
        response = []
        for row in results.fetchall():
            response.append(row)

    except sqlite3.Error as e:
        print('Failed to select data:', e)

    connection.commit()
    connection.close()

    return (response)

def get_live_data():
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    try:
        results = cursor.execute("SELECT kpl FROM rowOBDdata ORDER BY id DESC")
        respone = []
        for row in results.fetchall():
            respone.append(row)

    except sqlite3.Error as e:
        print('Failed to select data:', e)

    connection.commit()
    connection.close()

    return (respone)