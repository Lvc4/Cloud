import datetime
from MyLibs import configure

logfile = configure.logfile

def log(message):
    now = datetime.datetime.now()
    log = str(now.strftime('%Y.%m.%d %H:%M:%S')) + '  -  ' + message
    log_file = open(logfile, 'a')
    log_file.write(log + '\n')
    log_file.close()
