# Adjust to where you have GAM
GAM=$HOME/bin/gam7/gam
$GAM redirect csv ./company_devices.csv print devices fields serialnumber company nopersonaldevices nodeviceusers
