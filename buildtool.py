#!/usr/bin/env python3

import sys
import os.path
import json

data = dict()
try:
    ENV = sys.argv[1]
    if os.path.isfile(sys.argv[1]):
        raise ValueError
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
    print('Build file is not specified', file=sys.stderr)
    exit(1)
except ValueError:
    print('Not a valid Json', file=sys.stderr)
    exit(1)

print(f'Building for {ENV} ENV...')
vars = data['variables']
print(vars)
