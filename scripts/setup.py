import os
import sys
import string
import shutil
from tqdm import tqdm
import json

setup_dirs = [
    'temp',
    'logs',
    ]

with open("scripts/config.json", "r") as jsonfile:
    data = json.load(jsonfile)

src_dir = os.getcwd()

def get_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


# Windows based function setup
def windows():
    # Gather all available drive letters and print to screen
    os.chdir(data.get('dest_dir'))

    for d in setup_dirs:
        if d not in os.listdir():
            os.makedirs(f'{d}')

    # Copy all files from the source to the destination
    if "scripts" not in os.listdir(data.get('dest_dir')):
        os.makedirs(f'{data.get("dest_dir")}/scripts')
        with tqdm(total=get_size(f'{src_dir}/scripts'),unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            for dirpath, dirnames, filenames in os.walk(f'{src_dir}/scripts'):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    shutil.copy(fp, f'{data.get("dest_dir")}/scripts/')
                    pbar.update(os.path.getsize(fp))
    else:
        print('Scripts already copied')



# Linux based function setup
def linux():
    print('Linux based setup')

# Mac based function setup
def mac():
    print('Mac setup TBD')

# Check which operating system is in use
user_os = sys.platform

# Based on the operating system, run operating system specific setup
if user_os == 'win32':
    windows()
elif user_os == 'linux':
    linux()
elif user_os == 'darwin':
    mac()
else:
    print('Operating system not supported')


