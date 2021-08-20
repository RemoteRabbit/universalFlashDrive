import requests
from bs4 import BeautifulSoup
import os
import sys
from tqdm import tqdm
import hashlib
import tempfile
import configparser
import shutil


'''
When called we check which OS is running on host
and call the corresponding function
which will pass in a path argument to the corresponding ISO
function which will download the ISO to that path dependent on OS
'''

config = configparser.ConfigParser()
with open('scripts/config.ini', 'r') as configFile:
    config.read_file(configFile)


def main():
    user_os = sys.platform
    if user_os in ['linux', 'win32']:
        ubuntu()
    else:
        print('Operating system not supported')


# Windows 10 ISOs have to be manually installed and updated

# Check if string is float number
def isfloat(value):
    return value.replace('.', '').isdigit()


def sha256Checksum(filename, sha256_file):
    sha256 = hashlib.sha256()

    with open(filename, 'rb') as f:
        data = f.read()
        if not data:
            print('File is empty')
        sha256.update(data)

    with open(sha256_file, 'r') as f:
        return sha256.hexdigest() in f.read()

# Get the latest ubuntu iso and downloading it to the iso folder


def ubuntu():
    release_url = 'https://releases.ubuntu.com/'
    release_req = requests.get(release_url)
    soup = BeautifulSoup(release_req.text, 'html.parser')
    recent_release = ''
    for link in soup.find_all('a'):
        release_number = (link.get('href'))[:-1]
        is_float_bool = isfloat(release_number)
        # Get last true in link
        if is_float_bool == True:
            recent_release = release_number
    # Check if the iso is already downloaded
    if os.path.isfile(f'{config["BASE"]["ventoy_drive"]}/ubuntu-{recent_release}-desktop-amd64.iso'):
        print(f'Ubuntu {recent_release} is already downloaded')
    else:
        urls = {
            f'ubuntu-{recent_release}-desktop-amd64.iso': f'https://releases.ubuntu.com/{recent_release}/ubuntu-{recent_release}-desktop-amd64.iso',
            'SHA256SUMS': f'https://releases.ubuntu.com/{recent_release}/SHA256SUMS'
        }

        temp_dir = tempfile.mkdtemp()

        # Download the iso
        for key, value in urls.items():
            print(f'Downloading {key}...')
            response = requests.get(value, stream=True)
            with open(os.path.join(temp_dir, f'{key}'), 'wb') as f:
                total_length = int(response.headers.get('content-length'))
                with tqdm(total=total_length, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                    for chunk in response.iter_content(chunk_size=1024):
                        pbar.update(len(chunk))
                        f.write(chunk)

        # Verify the downloaded iso with the SHA256SUM file
        if sha256Checksum(os.path.join(temp_dir, f'ubuntu-{recent_release}-desktop-amd64.iso'), os.path.join(temp_dir, 'SHA256SUMS')) is True:
            # Move the downloaded iso to Ventoy
            shutil.copyfile(os.path.join(temp_dir, f'ubuntu-{recent_release}-desktop-amd64.iso'),
                            f'{config["BASE"]["ventoy_drive"]}/ubuntu-{recent_release}-desktop-amd64.iso')
            print('ISO has been downloaded')
        else:
            print('SHA256SUM file is not authentic')

        print(f'Ubuntu {recent_release} is downloaded')


main()
