import sqlite3

dbname = '../dbConn/obd.db'

connection = sqlite3.connect(dbname)

def create(dbname):
    cursor = connection.cursor()

    try:
        cursor.execute("""CREATE TABLE rowOBDdata (
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
    cursor = connection.cursor()

    try:
        data = obd_data
        cursor.execute("INSERT INTO rowOBDdata (time, vss, maf, kpl) VALUES (?, ?, ?, ?)",
                       (data[0], data[1], data[2], data[3]))

    except sqlite3.Error as e:
        print('Failed to insert data:', e)

    connection.commit()

    return True


def get_history_data(list):
    try:
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        try:
            data = list
            response = []
            selectList = []
            count = 0

            if data[2] > 0 :
                results = cursor.execute("SELECT 0 ,strftime('%Y-%m-%d %H:%M', time), printf('%.2f', avg(kpl)), printf('%.2f', avg(vss)), printf('%.2f', avg(maf)) FROM rowOBDdata WHERE time >= ? AND time <= ? and id < ? GROUP BY strftime('%Y-%m-%d %H:%M', time) ORDER By id DESC LIMIT ?, ?",
                    (data[0], data[1], data[2], data[3], data[4]))

                #results = cursor.execute("SELECT id, time, vss, maf, kpl FROM rowOBDdata WHERE time >= ? AND time <= ? and id < ? ORDER BY id DESC LIMIT ?, ?",(data[0], data[1], data[2], data[3], data[4]))
                for row in results.fetchall():
                    selectList.append(row)
            else :
                results = cursor.execute(
                   "SELECT max(id),strftime('%Y-%m-%d %H:%M', time), printf('%.2f', avg(kpl)), printf('%.2f', avg(vss)), printf('%.2f', avg(maf)) FROM rowOBDdata WHERE time >= ? AND time <= ?  GROUP BY strftime('%Y-%m-%d %H:%M', time) ORDER BY id DESC LIMIT ?, ?",(data[0], data[1], data[3], data[4]))

                #results = cursor.execute(
                #    "SELECT id, time, vss, maf, kpl FROM rowOBDdata WHERE time >= ? AND time <= ? ORDER BY id DESC LIMIT ?, ?",(data[0], data[1], data[3], data[4]))
                for row in results.fetchall():
                    selectList.append(row)
                countList = cursor.execute(
                           "SELECT count(*) FROM (SELECT strftime('%Y-%m-%d %H:%M', time) FROM rowOBDdata WHERE time >= ? AND time <= ? GROUP BY strftime('%Y-%m-%d %H:%M', time)) ",(data[0], data[1]))
               # countList = cursor.execute(
                #    "SELECT count(*) FROM rowOBDdata WHERE time >= ? AND time <= ?",(data[0], data[1]))
                count = countList.fetchone()[0]
                if count is None :
                    count = 0
        except sqlite3.Error as e:
            print('Failed to select data:', e)

        finally:
            cursor.close()
    finally:
        conn.close()

    response.append(selectList)
    response.append(count)
    return (response)

def get_live_data():
    try:
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        try:
            results = cursor.execute("SELECT time,kpl,vss,maf FROM rowOBDdata ORDER BY id DESC LIMIT 1")
            respone = results.fetchone()
        except sqlite3.Error as e:
            print('Failed to select data:', e)
        finally:
            cursor.close()
    finally:
        conn.close()
    return (respone)

