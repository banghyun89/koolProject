import sqlite3

dbname = '../dbConn/obd.db'

connection = sqlite3.connect(dbname)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create(dbname):
    cursor = connection.cursor()

    try:
        cursor.execute("""CREATE TABLE rowOBDdata (
                             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                             time DATE NOT NULL,
                             vss FLOAT NULL,
                             maf FLOAT NULL,
                             rpm FLOAT NULL,
                             kpl FLOAT NULL,
                             coolant_temp FLOAT NULL,
                             fuel_level FLOAT NULL,
                             ambient_air_temp FLOAT NULL,
                             oil_temp FLOAT NULL,
                             control_module_voltage FLOAT NULL,
                             intake_temp FLOAT NULL
                             );""")


    except sqlite3.Error as e:
        print('Failed to creat table:', e)

    connection.commit()
    connection.close()

    return True


def put_data(obd_data):
    sql = """
             INSERT INTO rowOBDdata (time,
                                      vss,
                                      maf,
                                      kpl,
                                      rpm,
                                      coolant_temp,
                                      fuel_level,
                                      ambient_air_temp,
                                      oil_temp,
                                      control_module_voltage,
                                      intake_temp)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          """
    cursor = connection.cursor()

    try:
        data = obd_data
        cursor.execute(sql,
                       (data['time'],
                        data['vss'],
                        data['maf'],
                        data['kpl'],
                        data['rpm'],
                        data['coolant_temp'],
                        data['fuel_level'],
                        data['ambient_air_temp'],
                        data['oil_temp'],
                        data['control_module_voltage'],
                        data['intake_temp']))

    except sqlite3.Error as e:
        print('Failed to insert data:', e)

    connection.commit()

    return True

def get_history_data(list):
    pagingSql = """
                     SELECT 0,
                            strftime('%Y-%m-%d %H:%M', time) as time,
                            printf('%.2f', avg(kpl)) as kpl,
                            printf('%.2f', avg(vss)) as vss,
                            printf('%.2f', avg(maf)) as maf,
                            printf('%.2f', avg(rpm)) as rpm,
                            printf('%.2f', avg(fuel_level)) as fuel_level,
                            printf('%.2f', avg(control_module_voltage)) as control_module_voltage,
                            printf('%.2f', avg(coolant_temp)) as coolant_temp,
                            printf('%.2f', avg(ambient_air_temp)) as ambient_air_temp,
                            printf('%.2f', avg(oil_temp)) as oil_temp,
                            printf('%.2f', avg(intake_temp)) as intake_temp
                       FROM rowOBDdata
                      WHERE time >= ?
                        AND time <= ?
                        AND id < ?
                   GROUP BY strftime('%Y-%m-%d %H:%M', time)
                   ORDER BY id DESC
                   LIMIT ?, ?
                """
    firstCallSql = """
                     SELECT max(id),
                            strftime('%Y-%m-%d %H:%M', time) as time,
                            printf('%.2f', avg(kpl)) as kpl,
                            printf('%.2f', avg(vss)) as vss,
                            printf('%.2f', avg(maf)) as maf,
                            printf('%.2f', avg(rpm)) as rpm,
                            printf('%.2f', avg(fuel_level)) as fuel_level,
                            printf('%.2f', avg(control_module_voltage)) as control_module_voltage,
                            printf('%.2f', avg(coolant_temp)) as coolant_temp,
                            printf('%.2f', avg(ambient_air_temp)) as ambient_air_temp,
                            printf('%.2f', avg(oil_temp)) as oil_temp,
                            printf('%.2f', avg(intake_temp)) as intake_temp
                       FROM rowOBDdata
                      WHERE time >= ?
                        AND time <= ?
                      GROUP BY strftime('%Y-%m-%d %H:%M', time)
                      ORDER BY id DESC
                      LIMIT ?, ?
                   """
    totalCountSql = """
                        SELECT count(*) totalCount
                          FROM (SELECT strftime('%Y-%m-%d %H:%M', time)
                                  FROM rowOBDdata
                                 WHERE time >= ?
                                   AND time <= ?
                                 GROUP BY strftime('%Y-%m-%d %H:%M', time))
                    """

    try:
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        try:
            data = list
            response = []
            selectList = []
            count = 0

            if data[2] > 0 : # paging sql when scroll table in the live page
                results = cursor.execute(pagingSql, (data[0], data[1], data[2], data[3], data[4]))
                for row in results.fetchall():
                    selectList.append(row)
            else : # first call
                results = cursor.execute(firstCallSql,(data[0], data[1], data[3], data[4]))

                for row in results.fetchall():
                    selectList.append(row)
                countList = cursor.execute(totalCountSql,(data[0], data[1]))
                count = countList.fetchone()[0]
                if count is None:
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

    sql = """SELECT time,
                     printf('%.2f',vss) as vss,
                     printf('%.2f',maf) as maf,
                     printf('%.2f',kpl) as kpl,
                     printf('%.2f',rpm) as rpm,
                     printf('%.2f',fuel_level) as fuel_level,
                     printf('%.2f',coolant_temp) as coolant_temp,
                     printf('%.2f',ambient_air_temp) as ambient_air_temp,
                     printf('%.2f',oil_temp) as oil_temp,
                     printf('%.2f',control_module_voltage) as control_module_voltage,
                     printf('%.2f',intake_temp) as intake_temp
                FROM rowOBDdata
                ORDER BY id DESC
                LIMIT 1
           """
    try:
        conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cursor = conn.cursor()

        try:
            results = cursor.execute(sql)
            respone = results.fetchone()
            #print(respone)
        except sqlite3.Error as e:
            print('Failed to select data:', e)
        finally:
            cursor.close()
    finally:
        conn.close()
    return (respone)

