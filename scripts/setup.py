import os
import sys
import string
import shutil
from tqdm import tqdm
import configparser

config = configparser.ConfigParser()
with open ('scripts/config.ini', 'r') as configFile:
    config.read_file(configFile)

def get_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

# Gather all available drive letters and print to screen
if config['BASE']['os_name'] == 'win32':
    storage_drive = f'{config["BASE"]["storage_drive"]}:/'
elif config['BASE']['os_name'] == 'linux': 
    storage_drive = f'/mnt/{(config["BASE"]["storage_drive"]).lower()}'
elif config['BASE']['os_name'] == 'darwin':
    storage_drive = f'/Volumes/{(config["BASE"]["storage_drive"]).lower()}'
else:
    print('OS not supported')
    
os.chdir(storage_drive)

# mkdirs for setup_dirs if they do not exist
for d in list((config['BASE']['setup_dirs']).split(" ")):
    if d not in os.listdir():
        os.makedirs(f'{d}')

if "scripts" not in os.listdir(storage_drive):
    os.makedirs(f'{storage_drive}/scripts')
    with tqdm(total=get_size(f'{config["BASE"]["src_dir"]}/scripts'),unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        for dirpath, dirnames, filenames in os.walk(f'{config["BASE"]["src_dir"]}/scripts'):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                shutil.copy(fp, f'{storage_drive}/scripts/')
                pbar.update(os.path.getsize(fp))
else:
    print('Scripts already copied')




