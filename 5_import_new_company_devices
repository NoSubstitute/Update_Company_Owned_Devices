# The GAM command needs a reference to the source file and the device type supplied when the script is run.
# The Asset Tag is recommended, so this command will pull the tag from the CSV and assign it to each device.
#
# The following device types are valid.
# ANDROID, CHROME_OS, GOOGLE_SYNC, IOS, LINUX, MAC_OS, WINDOWS
#
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <CSV_FILE> <DEVICE_TYPE>"
    echo "Valid device types: ANDROID, CHROME_OS, GOOGLE_SYNC, IOS, LINUX, MAC_OS, WINDOWS"
    exit 1
fi

# Adjust the GAM value to where you have GAM
GAM=$HOME/bin/gam7/gam
$GAM csv $1 gam create device serialnumber "~~Serial Number~~" devicetype $2 assettag "~~Asset Tag~~"
