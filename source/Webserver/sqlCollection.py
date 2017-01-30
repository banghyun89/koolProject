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


def get_history_data(list):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    try:
        data = []
        response = []
        response2 = []
        selectList = []
        count = 0
        for i in list:
            data.append(i)
        if data[2] > 0 :
            results = cursor.execute("SELECT id, time, vss, maf, kpl FROM rowOBDdata WHERE time >= ? AND time < ? and id < ? ORDER BY id DESC LIMIT ?, ?",(data[0], data[1], data[2], data[3], data[4]))
            for row in results.fetchall():
                selectList.append(row)
        else :
            results = cursor.execute(
                "SELECT id, time, vss, maf, kpl FROM rowOBDdata WHERE time >= ? AND time < ? ORDER BY id DESC LIMIT ?, ?",(data[0], data[1], data[3], data[4]))
            for row in results.fetchall():
                selectList.append(row)

            countList = cursor.execute(
                "SELECT count(*) FROM rowOBDdata WHERE time >= ? AND time < ?",(data[0], data[1]))
            for row in countList.fetchall():
                response2.append(row)
            if len(response2) > 0 :
                count = response2[0]


    except sqlite3.Error as e:
        print('Failed to select data:', e)

    connection.commit()
    connection.close()

    response.append(selectList)
    response.append(count)
    return (response)

def get_live_data():
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    try:
        results = cursor.execute("SELECT time,kpl,vss,maf FROM rowOBDdata ORDER BY id DESC LIMIT 1")
        respone = []
        for row in results.fetchall():
            respone.append(row)

    except sqlite3.Error as e:
        print('Failed to select data:', e)

    connection.commit()
    connection.close()

    return (respone)
