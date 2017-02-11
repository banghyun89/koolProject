import sys
sys.path.append("..")
import obd
import time
import termios
import random
from dbConn import sqlCollection
from obd.OBDResponse import OBDResponse

connection = obd.OBD('/dev/pts/1')
# connection = obd.OBD('/dev/rfcomm0') # auto-connects to USB or RF port

cmd1 = obd.commands.SPEED   # select an OBD command (sensor) Unit.kph ; km/h range : 0~1000
cmd2 = obd.commands.INTAKE_PRESSURE     # select an OBD command (sensor) Mass Air Flow g/s
cmd3 = obd.commands.INTAKE_TEMP     # select an OBD command (sensor) Mass Air Flow g/s
cmd4 = obd.commands.RPM     # select an OBD command (sensor) Mass Air Flow g/s
cmd5 = obd.commands.MAF     # select an OBD command (sensor) Mass Air Flow g/s
cmd6 = obd.commands.COOLANT_TEMP
cmd7 = obd.commands.FUEL_LEVEL
cmd8 = obd.commands.AMBIANT_AIR_TEMP
cmd9 = obd.commands.OIL_TEMP
cmd10 = obd.commands.CONTROL_MODULE_VOLTAGE

dataList = {}


def mafCalculation(rpmMagnitude, mapMagnitude, iatMagnitude):
    imap = rpmMagnitude * mapMagnitude / iatMagnitude
    stuff1 = .85
    stuff2 = (28.9644 / 8.314472)

    # print("STUFF1: ", stuff1, " STUFF2: ", stuff2)

    # stuff = (85/100)*(3.342)*(28.9644/8.314472)
    stuff = stuff1 * (3.342) * stuff2
    # print("STUFF: ", stuff)

    return round((imap/120)*stuff,2)

'''This block sets the MAF flag for the while loop -- if it evaluates true then calculations will run
NOTE: FALSE means the data cannot be pulled from the OBD'''
mafFail = False

try:
    maf = connection.query(cmd5)
    if maf is None or maf.value is None:
        mafFail = True
except:
    pass



while 1:
    try:
        vss = connection.query(cmd1) # send the command, and parse the response
        iat = connection.query(cmd3)
        rpm = connection.query(cmd4)
        coolTemp = connection.query(cmd6)
        fuelLevel = connection.query(cmd7)
        airTemp = connection.query(cmd8)
        oilTemp = connection.query(cmd9)
        conModVolt = connection.query(cmd10)

        if (rpm is None or rpm.value is None) or (vss is None or vss.value is None):
            continue

        if mafFail:
                map = connection.query(cmd2)
                maf = mafCalculation(rpm.value.magnitude, map.value.magnitude, iat.value.magnitude)
        else:
            maf = connection.query(cmd5)
            maf = maf.value.magnitude

        if (vss.value.magnitude > 300) or (maf >700):
            continue

    #    print(airTemp)
    #   print(oilTemp)
    #    print(conModVolt)

        currentTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(vss.time))
#        print(currentTime)

#        print("RPM: " , rpm.value.magnitude)
#      print("MAP: " , map.value.magnitude)
#      print("IAT: " , iat.value.magnitude)
#       print("MAF: " , maf)

        kpl = round(3.0215 * vss.value.magnitude / maf, 2)

        if (oilTemp is None or oilTemp.value is None) or (conModVolt is None or conModVolt.value is None) :
            oilTemp = 0
            conModVolt = 0
        else:
            oilTemp = oilTemp.value.magnitude
            conModVolt = conModVolt.value.magnitude

        dataList['time'] = currentTime
        dataList['kpl'] = kpl
        dataList['vss'] = vss.value.magnitude
        dataList['maf'] = maf
        dataList['rpm'] = rpm.value.magnitude
        dataList['coolant_temp'] = coolTemp.value.magnitude
        dataList['fuel_level'] = fuelLevel.value.magnitude
        dataList['ambient_air_temp'] = airTemp.value.magnitude
        dataList['intake_temp'] = iat.value.magnitude
        dataList['oil_temp'] = oilTemp
        dataList['control_module_voltage'] = conModVolt

    #   print(vss.value.magnitude)
    #   print(maf.value.magnitude)


        print(dataList)
        print('')

        #dbinsert
        sqlCollection.put_data(dataList)

        dataList = {}

    #    print(1/kpl)
    #    valStr = str(kpl)
    #    print(valStr + " kpl")
        time.sleep(1)

    except termios.error:
        continue