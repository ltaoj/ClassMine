import sys, os
print(os.path.dirname(os.path.realpath(__file__)))

configpath = os.path.dirname(os.path.realpath(__file__)).replace(os.path.sep + 'tests', '')
sys.path.append(configpath)

import login
