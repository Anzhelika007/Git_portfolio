from subprocess import call
from shutil import rmtree

try:
    rmtree('migrations')
except Exception:
    pass

command = "flask db init"

res = call(command, shell=True)

command = "flask db migrate"

res = call(command, shell=True)

command = "flask db upgrade"

res = call(command, shell=True)
