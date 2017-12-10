from pymultiwii import MultiWii

print("# Connect to Flydu..")
board = MultiWii("/dev/ttyS0")
try:
    print("# Try to send cmd..")
    testData = [0,0,0,0]

    # length of data, command, list with data.
    board.sendCMD(4, MultiWii.SET_RAW_RC, testData)
except Exception, error:
    print("# Error on board test: ", str(error))
