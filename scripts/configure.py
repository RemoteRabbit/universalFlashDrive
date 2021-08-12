import sys 
import os
import configparser


config = configparser.ConfigParser()
os_name = sys.platform
src_dir = os.getcwd()

# Base dirs to be made on build, separate each dir with a space
setup_dirs = 'tmp logs'

def get_win_drives():
    """
    Return a list of all available drives
    """
    import win32api
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\\\x00')[:-1]
    return [d for d in drives if os.path.exists(d)]


def get_linux_drives():
    """
    Return a list of all available drives
    * will need to distinguish between wsl and native
    """
    return [f'{dev.upper()}:' for dev in os.listdir('/mnt/') if dev]


# Get list of all mac drives
def get_mac_drives():
    """
    Return string for storage volume to validate it is present
    """
    try:
        for drive in os.listdir('/Volumes/'):
            if os.path.isdir('/Volumes/storage'):
                return drive
    except:
        print('No mac drive "storage" found')
    

def available_drives():
    """
    Return a list of all available drives based on OS
    """
    platform = sys.platform
    if platform == 'win32':
        return get_win_drives()
    elif platform == 'linux':
        return get_linux_drives()
    elif platform == 'darwin':
        return get_mac_drives()
    else:
        print('Operating system not supported')

while True:
    # If user is coming from mac, auto-select the storage volume.
    # If user is coming from windows or linux, have user select drive.
    if os_name == 'darwin':
        print(f'Mac detected \nAdding {available_drives()} to config.')
        flash_drive = available_drives()
        break
    else:
        drive_letter = input(f'{available_drives()} \nPlease select a drive letter for storage: ').upper()
        if (f'{drive_letter}:') not in available_drives():
            print('Invalid drive letter')
            continue
        else:
            flash_drive = drive_letter
            break       

# Build out OS section of config.ini file
config['BASE'] = {
    'os_name': os_name,
    'drive_letter': flash_drive,
    'src_dir': src_dir,
    'setup_dirs': setup_dirs
}

# Write config.ini file
with open('scripts/config.ini', 'w') as configfile:
    config.write(configfile)
