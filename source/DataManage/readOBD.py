import obd
import time
#import saveOBD

connection = obd.OBD('/dev/pts/4') # auto-connects to USB or RF port
cmd1 = obd.commands.SPEED   # select an OBD command (sensor)
cmd2 = obd.commands.MAF     # select an OBD command (sensor)

dataList = []


while 1:
    try:
        vss = connection.query(cmd1) # send the command, and parse the response
        maf = connection.query(cmd2)

        if (vss is None) or (maf is None):
            continue

    #   print(vss)
    #   print(maf)

        currentTime = time.strftime("%Y%m%d_%H:%M:%S",time.localtime(vss.time))
#        print(currentTime)
        dataList.append(currentTime)
        dataList.append(vss.value.magnitude)
        dataList.append(maf.value.magnitude)

    #   print(vss.value.magnitude)
    #   print(maf.value.magnitude)
        kpl = 30.215 * ((vss.value.magnitude) / (maf.value.magnitude))

        dataList.append(kpl)

        print(dataList)
        print('')

        """
        insertDB(dataList)     DB insert 부분
        """

        dataList = []

    #    print(1/kpl)
    #    valStr = str(kpl)
    #    print(valStr + " kpl")
        time.sleep(1)

    except IOError as e:
        print(e)

#sqlite> .save FILE   ee

#
# obd.OBD            # main OBD connection class
# obd.Async          # asynchronous OBD connection class
# obd.commands       # command tables
# obd.Unit           # unit tables (a Pint UnitRegistry)
# obd.OBDStatus      # enum for connection status
# obd.scan_serial    # util function for manually scanning for OBD adapters
# obd.OBDCommand     # class for making your own OBD Commands
# obd.ECU            # enum for marking which ECU a command should listen to
# obd.logger         # the OBD module's root logger (for debug)


# from obd import OBDCommand, Unit
# from obd.protocols import ECU
# from obd.utils import bytes_to_int
#
# def rpm(messages):
#     """ decoder for RPM messages """
#     d = messages[0].data
#     v = bytes_to_int(d) / 4.0  # helper function for converting byte arrays to ints
#     return v * Unit.RPM # construct a Pint Quantity
#
# c = OBDCommand("RPM", \          # name
#                "Engine RPM", \   # description
#                b"010C", \        # command
#                2, \              # number of return bytes to expect
#                rpm, \            # decoding function
#                ECU.ENGINE, \     # (optional) ECU filter
#                True)             # (optional) allow a "01" to be added for speed