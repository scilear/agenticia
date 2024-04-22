import os, sys, subprocess
if sys.platform.startswith('win'):
    os.system('.\flask_env\Scripts\activate')
else:
    subprocess.call(['bash', '-c', 'source flask_env/bin/activate'])