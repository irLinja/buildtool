#!/usr/bin/env python3

import sys
import os.path
import json
import re

regex_pattern = r'''<.*?>'''

try:
    if os.path.isfile(sys.argv[1]):
        raise ValueError
    ENV = sys.argv[1]
except ValueError:
    print('Probably you are missing an ENVIRONMENT name!', file=sys.stderr)
    exit(1)
except IndexError:
    print('No ENVIRONMENT name or BUILD FILE present')
    exit(1)
 
try:
    with open(sys.argv[2]) as json_file:
        data = json.load(json_file)
except IndexError:
    print(f'Build Environment is {ENV} but Build file is not specified', file=sys.stderr)
    exit(1)
except ValueError:
    print('Not a valid Json', file=sys.stderr)
    exit(1)

print(f'Building for {ENV} ENV...')

def get_env_value(environment, key):
    value = os.getenv( ENV + '_' + key)
    if value is None:
        value = os.getenv(key, 'undefined_variable')
    return value

files = data['templates']
variables = data['variables']
for sample_file in files.keys():
    with open(sample_file, 'r') as template:
        output_lines = list()
        for line in template.readlines():
            keys = re.findall(regex_pattern, line)
            if len(keys) == 0:
                newline = line
            else:
                for key in keys:
                    if key[1:-1] in variables:
                        newline = re.sub(key, get_env_value(ENV, key[1:-1]), line)
            output_lines.append(newline)

    with open(files.get(sample_file), 'w') as output:
        output.writelines(output_lines)
        print(f'{files.get(sample_file)} created/updated successfully')

exit(0)