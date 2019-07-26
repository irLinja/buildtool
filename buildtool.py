#!/usr/bin/env python3
'''
This is just a script to replace environment variables
based on ENVIRONMENT you are going to build for in you
application config files.
'''

import sys
import os.path
import json
import re

REGEX_PATTERN = r'''<.*?>'''

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
        DATA = json.load(json_file)
except IndexError:
    print('Build Environment is %s but Build file is not specified' % ENV, \
        file=sys.stderr)
    exit(1)
except ValueError:
    print('Not a valid Json', file=sys.stderr)
    exit(1)
except FileNotFoundError:
    print('Build file not found', file=sys.stderr)
    exit(1)

print('Building for %s ENV...' % ENV)


def get_env_value(environment, name):
    '''Finds and returns `environment_name` or `name` value from OS environment variables.'''
    value = os.getenv(environment + '_' + name)
    if value is None:
        value = os.getenv(name)
    if value is None:
        print('%s variable NOT Found' % name, file=sys.stderr)
        exit(2)
    return value

FILES = DATA['templates']
VARIABLES = DATA['variables']
for sample_file in FILES.keys():
    with open(sample_file, 'r') as template:
        output_lines = list()
        for line in template.readlines():
            keys = re.findall(REGEX_PATTERN, line)
            if not keys:
                newline = line
            else:
                for key in keys:
                    if key[1:-1] in VARIABLES:
                        newline = re.sub(key, get_env_value(ENV, key[1:-1]),\
                            line)
                        line = newline
                    else:
                        newline = " "
                        line = " "
            output_lines.append(newline)

    with open(FILES.get(sample_file), 'w') as output:
        output.writelines(output_lines)
        print('%s created/updated successfully' % FILES.get(sample_file))

exit(0)
