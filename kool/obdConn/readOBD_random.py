import sys
sys.path.append('..')
#import obd
import time
import random
from dbConn import sqlCollection

#connection = obd.OBD('/dev/cu.OBDKeyPro-DevB-1') # auto-connects to USB or RF port
#cmd1 = obd.commands.SPEED   # select an OBD command (sensor) Unit.kph ; km/h range : 0~1000
#cmd2 = obd.commands.MAF     # select an OBD command (sensor) Mass Air Flow g/s

cmd1 = 'SPEED'
cmd2 = 'MAF'
cmd3 = 'RPM'
cmd4 = 'COOLANT_TEMP'
cmd5 = 'FUEL_LEVEL'
cmd6 = 'AMBIENT_AIR_TEMP'
cmd7 = 'OIL_TEMP'
cmd8 = 'CONTROL_MODULE_VOLTAGE'
cmd9 = 'INTAKE_TEMP'
inputDict = {}
sensorDict = {  'SPEED': {'min':30,'max':250},
                'MAF': {'min':0,'max':100},
                'RPM': {'min':0,'max':100},
                'COOLANT_TEMP': {'min':0,'max':100},
                'FUEL_LEVEL': {'min':0,'max':100},
                'AMBIENT_AIR_TEMP': {'min':0,'max':100},
                'OIL_TEMP': {'min':0,'max':100},
                'CONTROL_MODULE_VOLTAGE': {'min':0,'max':100},
                'INTAKE_TEMP': {'min':0,'max':100}
              }

class valueObj:
    def __init__(self, number):
        self.magnitude = number

class cmdObj:
    def __init__(self, number):
        self.time = time.time()
        self.value = valueObj(number)

class obdObj:
    def query(self,sensorName):
        return cmdObj(round(random.uniform(sensorDict[sensorName]['min'],sensorDict[sensorName]['max']), 2))

connection = obdObj()

while 1:
    try:
        vss = connection.query(cmd1) # send the command, and parse the response
        maf = connection.query(cmd2)

        if (vss is None) and (maf is None):
            continue

        currentTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(vss.time))
        kpl = round( ((vss.value.magnitude) / (maf.value.magnitude)),2)

        inputDict['time'] = currentTime
        inputDict['kpl'] = kpl
        inputDict['vss'] = vss.value.magnitude
        inputDict['maf'] = maf.value.magnitude
        inputDict['rpm'] = connection.query(cmd3).value.magnitude
        inputDict['coolant_temp'] = connection.query(cmd4).value.magnitude
        inputDict['fuel_level'] = connection.query(cmd5).value.magnitude
        inputDict['ambient_air_temp'] = connection.query(cmd6).value.magnitude
        inputDict['oil_temp'] = connection.query(cmd7).value.magnitude
        inputDict['control_module_voltage'] = connection.query(cmd8).value.magnitude
        inputDict['intake_temp'] = connection.query(cmd9).value.magnitude

        print(inputDict)
        print('')

        #dbinsert
        sqlCollection.put_data(inputDict)

        dataList = []

        time.sleep(1)

    except IOError as e:
        print(e)
