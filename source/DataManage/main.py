# from datetime import datetime, timedelta
#
# today = datetime.today().strftime("%Y-%m-%d")
# now = datetime.now()
# a = int('1')
# timegap = timedelta(days=1)
# before = now - timegap
# after = now + timegap
# print("before==="+before.strftime('%Y-%m-%d') + "     after==="+ after.strftime('%Y-%m-%d'))
import sqlite3

time_cond_list = ['2017-01-27','2017-01-27']
connection = sqlite3.connect('obd.db')
cursor = connection.cursor()
try:
    data = []
    for i in time_cond_list:
        data.append(i)

    results = cursor.execute("SELECT time, vss, maf, kpl FROM rowOBDdata WHERE time >= ? AND time <= ?", (data[0], data[1]))
    response = []
    for row in results.fetchall():
        response.append(row)
        print("aaa=== "+row)

except sqlite3.Error as e:
    print('Failed to select data:', e)

connection.commit()
connection.close()

# import obd
# import sqlite3
#
# conn = sqlite3.connect('test.db')
# c = conn.cursor()
# # t = ('RHAT',)
# c.execute('SELECT * FROM tb1')
# print(c.fetchone())
# # Save (commit) the changes
# # conn.commit()
# conn.close()
#
# connection = obd.OBD() # auto-connects to USB or RF port
# cmd = obd.commands.SPEED # select an OBD command (sensor)
#
#
# response = connection.query(cmd) # send the command, and parse the response
# print(response.value) # returns unit-bearing values thanks to Pint
# print(response.value.to("mph")) # user-friendly unit conversions
#
#
#
# #sqlite> .save FILE
#
# #
# # obd.OBD            # main OBD connection class
# # obd.Async          # asynchronous OBD connection class
# # obd.commands       # command tables
# # obd.Unit           # unit tables (a Pint UnitRegistry)
# # obd.OBDStatus      # enum for connection status
# # obd.scan_serial    # util function for manually scanning for OBD adapters
# # obd.OBDCommand     # class for making your own OBD Commands
# # obd.ECU            # enum for marking which ECU a command should listen to
# # obd.logger         # the OBD module's root logger (for debug)
#
#
# # from obd import OBDCommand, Unit
# # from obd.protocols import ECU
# # from obd.utils import bytes_to_int
# #
# # def rpm(messages):
# #     """ decoder for RPM messages """
# #     d = messages[0].data
# #     v = bytes_to_int(d) / 4.0  # helper function for converting byte arrays to ints
# #     return v * Unit.RPM # construct a Pint Quantity
# #
# # c = OBDCommand("RPM", \          # name
# #                "Engine RPM", \   # description
# #                b"010C", \        # command
# #                2, \              # number of return bytes to expect
# #                rpm, \            # decoding function
# #                ECU.ENGINE, \     # (optional) ECU filter
# #                True)             # (optional) allow a "01" to be added for speed
#
