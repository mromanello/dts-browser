import multiprocessing

bind = "localhost:5051"
workers = 2#multiprocessing.cpu_count() * 2 + 1

reload=True
#accesslog='/var/log/flask/adele-app-access.log'
#errorlog='/var/log/flask/adele-app-error.log'
loglevel = 'debug'
proc_name='dts-demo-theses'

