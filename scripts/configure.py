import json
import sys 
import string
import os

build_config = {}

def add_config_item(key, value):
    build_config[key] = value

# Get OS type
add_config_item("os_name", sys.platform)

# Get Available drives
if build_config["os_name"] == "win32":
    # Get Dest Drive
    available_drives = [f'{d}:'for d in string.ascii_uppercase if os.path.exists(f'{d}:')]
    print(available_drives)
    while True:
        drive_letter = input('Please select a drive letter for storage: ')
        if (f'{drive_letter.upper()}:') not in available_drives:
            print('Invalid drive letter')
            continue
        else:
            add_config_item("dest_dir", f'{drive_letter.upper()}:/')
            break
elif build_config["os_name"] == "linux":
    print("Linux")
elif build_config["os_name"] == "darwin":
    print("OSX")
else:
    print("Unsupported OS")



jsonDump = json.dumps(build_config, indent=4)

with open('scripts/config.json', 'w') as json_data:
    json_data.write(jsonDump)
