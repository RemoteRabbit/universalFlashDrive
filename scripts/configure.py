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
    if sys.platform == 'win32':
        import win32api
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\\\x00')[:-1]
        return [d for d in drives if os.path.exists(d)]
    else:
        return []


def get_linux_drives():
    """
    Return a list of all available drives
    * will need to distinguish between wsl and native
    """
    if sys.platform == 'linux':
        return [f'{dev.upper()}:' for dev in os.listdir('/mnt/') if dev]
    else:
        return []


def available_drives():
    """
    Return a list of all available drives based on OS
    """
    platform = sys.platform
    if platform == 'win32':
        return get_win_drives()
    elif platform == 'linux':
        return get_linux_drives()
    else:
        print('Operating system not supported')


# Get user input for which drive to use
while True:
    drive_letter = input(
        f'{available_drives()} \nPlease select a drive letter for storage: ').upper()
    if (f'{drive_letter}:') not in available_drives():
        print('Invalid drive letter')
        continue
    else:
        flash_drive = drive_letter
        break

while True:
    drive_letter = input(
        f'{available_drives()} \nPlease select the Ventoy Drive letter: ').upper()
    if (f'{drive_letter}:') not in available_drives():
        print('Invalid drive letter')
        continue
    else:
        ventoy_drive = drive_letter
        break

# Section used to altering the few os specific settings
if os_name == 'win32':
    flash_drive = f'{flash_drive}:'
    ventoy_drive = f'{ventoy_drive}:'
elif os_name == 'linux':
    flash_drive = f'/mnt/{flash_drive.lower()}'
    ventoy_drive = f'/mnt/{ventoy_drive.lower()}'
else:
    print('Operating system not supported')

# Build out OS section of config.ini file
config['BASE'] = {
    'os_name': os_name,
    'drive_letter': flash_drive,
    'src_dir': src_dir,
    'setup_dirs': setup_dirs,
    'ventoy_drive': ventoy_drive
}

# Write config.ini file
with open('scripts/config.ini', 'w') as configfile:
    config.write(configfile)
