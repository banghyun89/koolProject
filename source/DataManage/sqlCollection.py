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

        cursor.execute("INSERT INTO rowOBDdata (time, vss, maf, kpl) VALUES (?, ?, ?, ?)",
                       (data[0], data[1], data[2], data[3]))

    except sqlite3.Error as e:
        print('Failed to insert data:', e)

    connection.commit()
    connection.close()

    return True


def get_history_data(time_cond_list):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    try:
        data = []
        for i in time_cond_list:
            data.append(i)
        results = cursor.execute("SELECT time, vss, maf, kpl FROM rowOBDdata WHERE time >= ? AND time <= ?",(data[0], data[1]))
        #results = cursor.execute("SELECT time, vss, maf, kpl FROM rowOBDdata WHERE time >= '2017-01-27' AND time <= '2017-01-27'")
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
        results = cursor.execute("SELECT kpl FROM rowOBDdata ORDER BY id DESC LIMIT 1")
        respone = []
        for row in results.fetchall():
            respone.append(row)

    except sqlite3.Error as e:
        print('Failed to select data:', e)

    connection.commit()
    connection.close()

    return (respone)