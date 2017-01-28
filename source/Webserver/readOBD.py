import obd
import time
import random
#import sqlCollection
from customPackage import sqlCollection

#connection = obd.OBD('/dev/cu.OBDKeyPro-DevB-1') # auto-connects to USB or RF port
#cmd1 = obd.commands.SPEED   # select an OBD command (sensor) Unit.kph ; km/h range : 0~1000
#cmd2 = obd.commands.MAF     # select an OBD command (sensor) Mass Air Flow g/s

cmd1 = 'cmd1'
cmd2 = 'cmd2'

dataList = []

class valueObj:
    def __init__(self, number):
        self.magnitude = number

class cmdObj:
    def __init__(self, number):
        self.time = time.time()
        self.value = valueObj(number)


class obdObj:
    def query(self,v):
        if v == 'cmd1' :
            return cmdObj(round(random.uniform(0, 400.99), 2)) #vss
        else :
            return cmdObj(round(random.uniform(0, 99.99), 2)) #maf

connection = obdObj()

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
