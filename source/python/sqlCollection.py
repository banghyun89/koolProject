import sqlite3

dbname = 'obd.db'

def tablecreate():
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    try:
        cursor.execute("""CREATE TABLE rowOBDdata (
                             rpm INTEGER PRIMARY KEY UNIQUE NOT NULL,
                             speed INTEGER NOT NULL,
                             maf INTEGER NOT NULL,
                             timedata DATE NOT NULL)""")

    except sqlite3.Error as e:
        print('Failed to creat table:', e)

    connection.commit()
    connection.close()

    return None

def tableselect():
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    try:
        results = cursor.execute("SELECT * FROM rowOBDdata")
        response = []
        for row in results.fetchall():
            response.append(row)

    except sqlite3.Error as e:
        print('Failed to select data:', e)

    connection.commit()
    connection.close()

    return (response)

def tableinsert(rpm, speed, maf, timedata):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    rpm = rpm
    speed = speed
    maf = maf
    timedata = timedata

    try:
        cursor.execute("INSERT INTO rowOBDdata (rpm, speed, maf, timedata) VALUES (?, ?, ?, ?)", (rpm, speed, maf, timedata))

    except sqlite3.Error as e:
        print('Failed to insert data:', e)

    connection.commit()
    connection.close()

    return None