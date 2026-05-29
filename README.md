# Update Company Owned Devices
Scripts to help you add devices from your MDM to the Company Owned Devices inventory in Google Workspace

## These are the scripts used.
1_export_company_devices.sh<br>
2_remove_duplicates.py<br>
3_export_mdm_devices.sh<br>
4_find_new_devices.py<br>
5_import_new_company_devices

## This is how they are used.
bash 1_export_company_devices.sh<br>
python3 2_remove_duplicates.py<br>
bash 3_export_mdm_devices.sh<br>
python3 4_find_new_devices.py company_devices_deduplicated.csv 2 MDM_devices.csv 1 new_devices.csv --asset-tag-value "Testing Only"<br>
bash 5_import_new_company_devices new_devices.csv MAC_OS

## The following device types are valid.
ANDROID, CHROME_OS, GOOGLE_SYNC, IOS, LINUX, MAC_OS, WINDOWS

# Example of the process
## Step 1 - export a list of company devices from Google Workspace
$ bash 1_export_company_devices.sh<br>
Getting all Company Devices, may take some time on a large Google Workspace Account...<br>
Got 1817 Company Devices...<br>

## Step 2 - deduplicate the exported list of company devices
$ python3 2_remove_duplicates.py<br>
Removed 80 duplicate rows.<br>
Deduplicated data saved to 'company_devices_deduplicated.csv'

## Step 3 - export your list of devices from your MDM or asset management system
$ bash 3_export_mdm_devices.sh<br>
Yeah, this step is all yours. :-)<br>
You need to create a csv file you can use in step 4 to compare with the exported Company Devices csv.<br>
I manually exported my list of devices from Mosyle to the file mosyle.csv.<br>
If you know how to pull such lists via API from different systems, please, post that code as [issues](https://github.com/NoSubstitute/Update_Company_Owned_Devices/issues).

## Step 4 - compare the two files and export the missing devices to new_devices.csv
$ Running 4_find_new_devices.py without parameters will give you an error.<br>
usage: 4_find_new_devices.py [-h] [--asset-tag-value ASSET_TAG_VALUE | --asset-tag-column ASSET_TAG_COLUMN]<br>
                             file1 col1 file2 col2_id output<br>
4_find_new_devices.py: error: the following arguments are required: file1, col1, file2, col2_id, output<br>

I must recommend always using an Asset Tag for each device, even though the code here allows you to not set one.<br>
Either an individual value for each device, based on a column in your MDM export, or the same for all, using one of the two available arguments.<br>

$ python3 4_find_new_devices.py company_devices_deduplicated.csv 2 mosyle.csv 1 new_devices.csv --asset-tag-value "Testing Only"<br>
Found 25 new devices.<br>
List of new devices saved to 'new_devices.csv'<br>

## Step 5 - create new company devices in Google Workspace
$ bash 5_import_new_company_devices new_devices.csv MAC_OS<br>
2026-05-29T15:32:07.636+02:00,0/25,Using 25 processes...<br>
2026-05-29T15:32:08.307+02:00,0,Processing item 25/25<br>
Company Device: /devices/???, deviceType: MAC_OS, serialNumber: 123456789, assetTag: Testing Only, Create Failed: Requested entity already exists<br>
Company Device: devices/CiQ4YTYwZDliMC1mNWIwLTQyMmItYTg1ZC1iNzlhZmZkNTEwNjI%3D, deviceType: MAC_OS, serialNumber: ABC98765, assetTag: Testing Only, Created<br>

# NOTE - THIS MAY NOT WORK FOR EVERYONE!
## Here's what the API documentation says for devices.create
https://docs.cloud.google.com/identity/docs/reference/rest/v1/devices/create

Method: devices.create<br>
Creates a device. Only company-owned device may be created.<br>
Note: This method is available only to customers who have one of the following SKUs: Enterprise Standard, Enterprise Plus, Enterprise for Education, and Cloud Identity Premium
