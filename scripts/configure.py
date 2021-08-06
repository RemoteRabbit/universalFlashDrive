import json
import sys 

build_config = {}

def get_os_name():
    build_config['os_name'] = sys.platform

get_os_name()

jsonDump = json.dumps(build_config, indent=4)

with open('scripts/config.json', 'w') as json_data:
    json_data.write(jsonDump)
