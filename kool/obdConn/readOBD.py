import sys
sys.path.append("..")
import obd
import time
import random
from dbConn import sqlCollection

connection = obd.OBD('/dev/pts/1') # auto-connects to USB or RF port
cmd1 = obd.commands.SPEED   # select an OBD command (sensor) Unit.kph ; km/h range : 0~1000
cmd2 = obd.commands.MAF     # select an OBD command (sensor) Mass Air Flow g/s

dataList = []

while 1:
    try:
        vss = connection.query(cmd1) # send the command, and parse the response
        maf = connection.query(cmd2)

        if (vss is None) and (maf is None):
            continue

    #   print(vss)
    #   print(maf)

        currentTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(vss.time))
#        print(currentTime)
        dataList.append(currentTime)
        dataList.append(vss.value.magnitude)
        dataList.append(maf.value.magnitude)

    #   print(vss.value.magnitude)
    #   print(maf.value.magnitude)
        kpl = round(30.215 * ((vss.value.magnitude) / (maf.value.magnitude)),2)
        dataList.append(kpl)

        print(dataList)
        print('')

        #dbinsert
        sqlCollection.put_data(dataList)

        dataList = []

    #    print(1/kpl)
    #    valStr = str(kpl)
    #    print(valStr + " kpl")
        time.sleep(1)

    except IOError as e:
        print(e)
