##########################################################################################
#                                                                                        #
#  PYTHON CODE TO RETRIEVE SOUNDING DATA FROM THE UNIVERSITY OF WYOMING ARCHIVE AND      #
#  THEN CONVERT THAT DATA INTO TABULAR FORMAT THAT CAN THEN BE LOADED INTO SHARPPY.      #
#  THIS ALGORITHM CAN BE CONFIGURED TO EITHER SAVE THE TABULAR DATA TO A FILE OR TO      #
#  DIRECTLY PASS IT TO SHARPPY.                                                          #
#                                                                                        #
#  Author: David Stang                                                                   #
#  Email:  david.w.stang-1@ou.edu                                                        #
#                                                                                        #
#  The entire algorithm has been distilled down into something that is accessible via a  #
#  single function call. See the end of the file for example calls. A web app has also   #
#  been built to perform the file-conversion function of this Python program:            #
#                                                                                        #
#  weather.ou.edu/~dscg1/sounding/                                                       #
#                                                                                        #
#  If you find either the Python program or the web app to be beneficial, please share   #
#  it with others who might also benefit from it.                                        #
#                                                                                        #
#                                                                                        #
#  List of key functions contained within this file:                                     #
#                                                                                        #
#    convertData(rawData, timeStamp)                                                     #
#      rawData:   The raw HTML content read from the University of Wyoming archive       #
#      timeStamp: The 10-digit timestamp used to look up the sounding data               #
#    FUNCTION:  convertData takes the University of Wyoming data and converts it to      #
#               tabular format (which is what SHARPpy uses).                             #
#                                                                                        #
#    retrieveData(timeStamp, location)                                                   #
#      timeStamp: The 10-digit timestamp corresponding to which sounding is desired      #
#      location:  The 5-digit station code corresponding to the sounding's location      #
#    FUNCTION:  retrieveData grabs sounding data from the University of Wyoming's        #
#               archives and then automatically passes it to convertData()               #
#               The original version of this Python program saves the converted data to  #
#               a file (within convertData()), but the converted data is also returned   #
#               at the end of the function call, so it is possible to automatically      #
#               pass the converted data into SHARPPy.                                    #
#                                                                                        #
##########################################################################################

import urllib.request


# Station object (part of a list that is initialized below)
class Station():
    def __init__(self, id, code, city, state):
        self.id = id
        self.code = code
        self.city = city
        self.state = state


# List of stations (most useful for user interface purposes)
STATION = [
  Station(72659, "ABR", "Aberdeen",            "SD"),
  Station(72518, "ALB", "Albany",              "NY"),
  Station(72365, "ABQ", "Albuquerque",         "NM"),
  Station(72363, "AMA", "Amarillo",            "TX"),
  Station(72230, "BMX", "Birmingham",          "AL"),
  Station(72764, "BIS", "Bismarck",            "ND"),
  Station(72318, "RNK", "Blacksburg",          "VA"),
  Station(72681, "BOI", "Boise",               "ID"),
  Station(72250, "BRO", "Brownsville",         "TX"),
  Station(72528, "BUF", "Buffalo",             "NY"),
  Station(72712, "CAR", "Caribou",             "ME"),
  Station(72649, "MPX", "Chanhassen",          "MN"),
  Station(72208, "CHS", "Charleston",          "SC"),
  Station(72251, "CRP", "Corpus Christi",      "TX"),
  Station(74455, "DVN", "Davenport",           "IA"),
  Station(72261, "DRT", "Del Rio",             "TX"),
  Station(72469, "DNR", "Denver",              "CO"),
  Station(72632, "DTX", "Detroit",             "MI"),
  Station(72451, "DDC", "Dodge City",          "KS"),
  Station(72364, "EPZ", "El Paso",             "TX"),
  Station(72582, "LKN", "Elko",                "NV"),
  Station(72376, "FGZ", "Flagstaff",           "AZ"), 
  Station(72249, "FWD", "Fort Worth",          "TX"),
  Station(72634, "APX", "Gaylord",             "MI"),
  Station(72768, "GGW", "Glasgow",             "MT"),
  Station(72476, "GJT", "Grand Junction",      "CO"),
  Station(74389, "GYX", "Gray",                "ME"),
  Station(72776, "TFX", "Great Falls",         "MT"),
  Station(72645, "GRB", "Green Bay",           "WI"),
  Station(72317, "GSO", "Greensboro",          "NC"),
  Station(72747, "INL", "International Falls", "MN"),
  Station(72235, "JAN", "Jackson",             "MS"),
  Station(72206, "JAX", "Jacksonville",        "FL"),
  Station(72201, "KEY", "Key West",            "FL"),
  Station(72240, "LCH", "Lake Charles",        "LA"),
  Station(74646, "LMN", "Lamont",              "OK"),
  Station(72388, "VEF", "Las Vegas",           "NV"),
  Station(74560, "ILX", "Lincoln",             "IL"),
  Station(72340, "LZK", "Little Rock",         "AR"),
  Station(72597, "MFR", "Medford",             "OR"),
  Station(72202, "MFL", "Miami",               "FL"),
  Station(72265, "MAF", "Midland",             "TX"),
  Station(72327, "BNA", "Nashville",           "TN"),
  Station(72233, "LIX", "New Orleans",         "LA"),
  Station(72305, "MHX", "Newport",             "NC"),
  Station(72357, "OUN", "Norman",              "OK"),
  Station(72562, "LBF", "North Platte",        "NE"),
  Station(72493, "OAK", "Oakland",             "CA"),
  Station(72558, "OAX", "Omaha",               "NE"),
  Station(72215, "FFC", "Peachtree City",      "GA"),
  Station(74626, "???", "Phoenix",             "AZ"),
  Station(72520, "PIT", "Pittsburgh",          "PA"),
  Station(72797, "UIL", "Quillayute",          "WA"),
  Station(72662, "RAP", "Rapid City",          "SD"),
  Station(72489, "REV", "Reno",                "NV"),
  Station(72672, "RIW", "Riverton",            "WY"),
  Station(72694, "SLE", "Salem",               "OR"),
  Station(72572, "SLC", "Salt Lake City",      "UT"),
  Station(72293, "NKX", "San Diego",           "CA"),
  Station(72248, "SHV", "Shreveport",          "LA"),
  Station(72786, "OTX", "Spokane",             "WA"),
  Station(72440, "SGF", "Springfield",         "MO"),
  Station(72403, "IAD", "Sterling",            "VA"),
  Station(72214, "TLH", "Tallahassee",         "FL"),
  Station(72210, "TBW", "Tampa Bay",           "FL"),
  Station(72456, "TOP", "Topeka",              "KS"),
  Station(72501, "OKX", "Upton",               "NY"),
  Station(72393, "VBG", "Vandenberg",          "CA"),
  Station(72402, "WAL", "Wallops Island",      "VA"),
  Station(72426, "ILN", "Wilmington",          "OH")
]


def convertData(rawData, timeStamp):
    c = 0

    # "DATA" will store a two-dimensional list of all the values extracted from the
    # table retrieved from the University of Wyoming's sounding archive.
    DATA = []

    theYear  = timeStamp[0:4]
    theMonth = timeStamp[4:6]
    theDay   = timeStamp[6:8]
    theHour  = timeStamp[8:10]

    theMonth = verifyLength(theMonth, 2)
    theDay   = verifyLength(theDay,   2)
    theHour  = verifyLength(theHour,  2)

    # The below timestamp will appear in the contents of the exported tabular data file
    theStamp = theYear[-2:] + theMonth + theDay + "/" + theHour + "00 "

    # Scan to find the header of the output
    while (rawData[c:c+4].upper() != "<H2>" and c < len(rawData) ):

        # A specific text string will appear in the response data if sounding data is
        # missing

        if (rawData[c:c+9].upper() == "CAN'T GET"):
            throwError("SOUNDING DATA NOT FOUND")
            return "ERROR"

        c = c + 1

    # Unexpected EOF (End Of File)
    if (c == len(rawData)):
       throwError("SOUNDING DATA NOT FOUND")
       return "ERROR"

    # Get the three letter code for the station
    stationID = rawData[c+10:c+13]

    # Scan to find the start of the data
    while (rawData[c:c+5].upper() != "<PRE>"):
        c = c + 1

    # lastHyphen will store the index where the numerical output first begins
    lastHyphen = -1
    dataTable = ""

    # Scan to find where the numerical output begins
    #
    # NOTE: DO NOT USE A SINGLE HYPHEN IN THE BELOW IF-STATEMENT, OTHERWISE NEGATIVE
    # NUMBERS WILL SCREW UP THE DATA RETRIEVAL PROCESS
    while (rawData[c:c+6].upper() != "</PRE>"):
        if (rawData[c:c+4] == "----"):
            lastHyphen = c+4

        c = c + 1

    # Found the extent of the data block, now scan through again...
    c = lastHyphen + 1

    # ...and pick out the table of numbers
    while (rawData[c:c+6].upper() != "</PRE>"):
        dataTable = dataTable + rawData[c]

        c = c + 1

    # Each measurement at each height is put on its own line
    # "buffer" will be used to generate a 2-D list of values
    dataArray = dataTable.split("\n")
    buffer = []

    pressure = 0
    lastPressure = -999
    windDir = -999

    for i in range(0, len(dataArray)):
        if (dataArray[i] == ""):
            continue

        pressure = stripNumber( dataArray[i][0 : 8] )
        windDir  = float( stripNumber( dataArray[i][42:50] ) )

        while (windDir >= 360):
            windDir = windDir - 360

        # SHARPpy will reject a data file that contains duplicate pressures. Make sure
        # the next pressure reading is different than the last one.
        if (pressure == lastPressure):
            continue

        # Slice out the segment of text on each line that contains the data we need and
        # store the results in a 6-element list
        buffer.append( pressure                           )    # Pressure (mb)
        buffer.append( stripNumber( dataArray[i][7 :15] ) )    # Height (m)
        buffer.append( stripNumber( dataArray[i][14:22] ) )    # Temperature (C)
        buffer.append( stripNumber( dataArray[i][21:29] ) )    # Dewpoint (C)
        buffer.append( windDir                            )    # Wind Direction (Deg)
        buffer.append( stripNumber( dataArray[i][49:57] ) )    # Wind Speed (kt)

        # Add the list to "DATA"
        DATA.append( buffer )

        lastPressure = pressure

        # Reset the "buffer" variable for the next line
        buffer = []

    # Header for the tabular data file
    exportData = "%TITLE%" + "\n " + stationID + "   " + theStamp + "\n   LEVEL       HGHT       TEMP       DWPT       WDIR       WSPD\n-------------------------------------------------------------------\n%RAW%\n"

    # Go through each observation parsed out and create a new table that matches the
    # format of a tabular data file
    for i in range(0, len(DATA)):
        exportData = exportData + fitLength( DATA[i][0], 8  ) + ","
        exportData = exportData + fitLength( DATA[i][1], 10 ) + ","
        exportData = exportData + fitLength( DATA[i][2], 10 ) + ","
        exportData = exportData + fitLength( DATA[i][3], 10 ) + ","
        exportData = exportData + fitLength( DATA[i][4], 10 ) + ","
        exportData = exportData + fitLength( DATA[i][5], 10 )
        exportData = exportData + "\n"

    # Closing mark for the tabular data file (IMPORTANT)
    exportData = exportData + "%END%"

    fileName = theYear + "-" + theMonth + "-" + theDay + " " + theHour + "00Z." + stationID

    # Save the data to a new file
    pointer = open(fileName, "w")
    pointer.write(exportData)
    pointer.close()

    return exportData

    
def retrieveData(timeStamp, stationID):
    year =  timeStamp[0:4]
    month = timeStamp[4:6]
    day =   timeStamp[6:8]
    hour =  timeStamp[8:10]

    # Web address for the archive corresponding to the given timestamp and station ID
    requestURL = "http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR="+year+"&MONTH="+month+"&FROM="+day+hour+"&TO="+day+hour+"&STNM="+str(stationID)

    try:
        # Get the data at the web address
        theData = urllib.request.urlopen(requestURL).read()
        theData = theData.decode('ascii')

        # And convert it
        newData = convertData(theData, timeStamp)

        return newData
    except:
        throwError("AN ERROR OCCURRED IN RETRIEVING THE DATA")
        return "ERROR"
        

# Function to strip the number element out of a string element
def stripNumber(theString):
    c = 0
    buffer = ""

    while ( c < len(theString) and not(isNumeric(theString[c])) ):
        c = c + 1

    while ( c < len(theString) and isNumeric(theString[c]) ):
        buffer = buffer + theString[c]
        c = c + 1

    # Missing data
    if (buffer == ""):
        buffer = "-9999.00"

    return buffer


def isNumeric(theChar):
    cc = ord(theChar)
    
    return ( (cc >= 0x30 and cc <= 0x39) or (cc == 0x2e) or (cc == 0x2d) )


# Method to ensure that numeric elements are certain number of digits long. This is
# important if a program is generating the timestamp from individual user inputs of
# year, month, day, and hour.
def verifyLength(theItem, theLength):
    newItem = str(theItem)

    while ( len(newItem) < theLength ):
        newItem = "0" + newItem

    return newItem


# Method to ensure that string elements have a certain amount of spacing. This is
# important when building data tables, because spacing has to be consistent.
def fitLength(theItem, theLength):
    newItem = str(theItem)

    while ( len(newItem) < theLength ):
        newItem = " " + newItem

    return newItem


def throwError(theError):
    print(theError)



# Timestamp is formatted as follows:
#
#             YYYYMMDDHH
#
# Please note this timestamp is in ZULU/UTC TIME.

# Sample function call specifically using the station ID
retrieveData("2019072712", 72230)

# Sample function call that pulls the station ID from the station list (more suitable for
# user interface purposes)
retrieveData("2019072712", STATION[0].id)

# Could also do:
# soundingData = retrieveData("2019072712", STATION[0].id)
# and then pass the variable soundingData to SHARPPy's plotting/interpretation function