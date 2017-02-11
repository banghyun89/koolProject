import sqlite3
import itertools

dbname = '../dbConn/obd.db'

connection = sqlite3.connect(dbname)

sensorDict = {'vss': 'vss', 'maf': 'maf', 'kpl': 'kpl', 'rpm': 'rpm', 'fuel_level': 'fuel_level',
              'coolant_temp': 'coolant_temp', 'ambient_air_temp': 'ambient_air_temp', 'oil_temp': 'oil_temp',
              'control_module_voltage': 'control_module_voltage', 'intake_temp': 'intake_temp'}

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
                     SELECT
                            strftime('%Y-%m-%d %H:%M', time) as time,
                            round( avg(kpl),2) as kpl,
                            round( avg(vss),2) as vss,
                            round( avg(maf),2) as maf,
                            round( avg(rpm),2) as rpm,
                            round( avg(fuel_level),2) as fuel_level,
                            round( avg(control_module_voltage),2) as control_module_voltage,
                            round( avg(coolant_temp),2) as coolant_temp,
                            round( avg(ambient_air_temp),2) as ambient_air_temp,
                            round( avg(oil_temp),2) as oil_temp,
                            round( avg(intake_temp),2) as intake_temp
                       FROM rowOBDdata
                      WHERE time >= ?
                        AND time <= ?
                        AND id < ?
                   GROUP BY strftime('%Y-%m-%d %H:%M', time)
                   ORDER BY id DESC
                   LIMIT ?, ?
                """
    firstCallSql = """
                     SELECT
                            strftime('%Y-%m-%d %H:%M', time) as time,
                            round( avg(kpl),2) as kpl,
                            round( avg(vss),2) as vss,
                            round( avg(maf),2) as maf,
                            round( avg(rpm),2) as rpm,
                            round( avg(fuel_level),2) as fuel_level,
                            round( avg(control_module_voltage),2) as control_module_voltage,
                            round( avg(coolant_temp),2) as coolant_temp,
                            round( avg(ambient_air_temp),2) as ambient_air_temp,
                            round( avg(oil_temp),2) as oil_temp,
                            round( avg(intake_temp),2) as intake_temp
                       FROM rowOBDdata
                      WHERE time >= ?
                        AND time <= ?
                      GROUP BY strftime('%Y-%m-%d %H:%M', time)
                      ORDER BY id DESC
                      LIMIT ?, ?
                   """
    firstCallSqlMaxId = """
                     SELECT max(id) as maxId
                       FROM rowOBDdata
                      WHERE time >= ?
                        AND time <= ?
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
            maxId = 0

            if data[2] > 0 : # paging sql when scroll table in the live page
                results = cursor.execute(pagingSql, (data[0], data[1], data[2], data[3], data[4]))
                for row in results.fetchall():
                    selectList.append(row)
            else : # first call
                results = cursor.execute(firstCallSql,(data[0], data[1], data[3], data[4]))

                for row in results.fetchall():
                    selectList.append(row)

                results2 = cursor.execute(firstCallSqlMaxId, (data[0], data[1]))
                maxId = results2.fetchone()[0]

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
    response.append(maxId)
    return (response)

def get_history_data_list(list):

    sqlDict =   {"groupByMinute":" GROUP BY strftime('%Y-%m-%d %H:%M', time) ",
                  "groupByDay" : " GROUP BY strftime('%Y-%m-%d', time) ",
                  "bottom1" :" FROM rowOBDdata WHERE time >= ? AND time <= ? ",
                  "bottom2": "ORDER BY id ASC",
                  "timeByMinute" : "SELECT strftime('%H:%M', time) as time, ",
                  "timeByDay": "SELECT strftime('%Y-%m-%d', time) as time, ",
                  "columnPrefix1" : " round( avg(",
                  "columnPrefix2": "),2) "
                 }
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
            period = int(data[2])
            selectColList = data[3]
            sqlColumnList = [sqlDict["columnPrefix1"]+sensorDict[x]+sqlDict["columnPrefix2"] for x in selectColList]
            selectColList.insert(0, "time")

            if period > 0 :
                groupby = sqlDict["groupByDay"]
                timesql = sqlDict["timeByDay"]
            else :
                groupby = sqlDict["groupByMinute"]
                timesql = sqlDict["timeByMinute"]


            sql = timesql\
                + ",".join(sqlColumnList)\
                + sqlDict["bottom1"]\
                + groupby\
                + sqlDict["bottom2"]
            print(sql)
            results = cursor.execute(sql,(data[0], data[1]))
            for row in results.fetchall():
                selectList.append(row)
            countList = cursor.execute(totalCountSql,(data[0], data[1]))
            count = countList.fetchone()[0]

            rsList = []
            for columns in itertools.izip_longest(*selectList, fillvalue=''):
                rsList.append(columns)


        except sqlite3.Error as e:
            print('Failed to select data:', e)

        finally:
            cursor.close()
    finally:
        conn.close()

    response.append(selectColList)
    response.append(rsList)
    response.append(count)

    return (response)

def get_live_data():


    sql = """SELECT time,
                     round(vss,2) as vss,
                     round(maf,2) as maf,
                     round(kpl,2) as kpl,
                     round(rpm,2) as rpm,
                     round(fuel_level,2) as fuel_level,
                     round(coolant_temp,2) as coolant_temp,
                     round(ambient_air_temp,2) as ambient_air_temp,
                     round(oil_temp,2) as oil_temp,
                     round(control_module_voltage,2) as control_module_voltage,
                     round(intake_temp,2) as intake_temp
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


def get_live_data_chart(sensor):

    sensor = sensorDict[sensor]

    sql1 = "SELECT "\
           + "       round(max(" + sensor + "),2) as maxValue,"\
           + "       round(min(" + sensor + "),2) as minValue,"\
           + "       round(avg(" + sensor + "),2) as avgValue"\
           + " FROM rowOBDdata "\
           + " WHERE time >= strftime('%Y-%m-%d','now','localtime') " \
           + " ORDER BY id DESC"

    sql2 = """SELECT time,
                     round(vss,2) as vss,
                     round(maf,2) as maf,
                     round(kpl,2) as kpl,
                     round(rpm,2) as rpm,
                     round(fuel_level,2) as fuel_level,
                     round(coolant_temp,2) as coolant_temp,
                     round(ambient_air_temp,2) as ambient_air_temp,
                     round(oil_temp,2) as oil_temp,
                     round(control_module_voltage,2) as control_module_voltage,
                     round(intake_temp,2) as intake_temp
                FROM rowOBDdata
                ORDER BY id DESC
                LIMIT 1
           """
    try:
        conn = sqlite3.connect(dbname)
        conn.row_factory = dict_factory
        cursor = conn.cursor()

        try:
            results1 = cursor.execute(sql1)
            respone1 = results1.fetchone()

            results2 = cursor.execute(sql2)
            respone2 = results2.fetchone()

            respone2['maxValue'] = respone1['maxValue']
            respone2['minValue'] = respone1['minValue']
            respone2['avgValue'] = respone1['avgValue']
        except sqlite3.Error as e:
            print('Failed to select data:', e)
        finally:
            cursor.close()
    finally:
        conn.close()
    return (respone2)
