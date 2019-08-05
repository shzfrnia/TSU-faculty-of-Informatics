#!//usr/local/bin/python3
import sys
from app import app

args = sys.argv
allowedFlags = frozenset({'-d', '-p', '-help'})
debug_mode = False
my_port = 5000
help_info = {
    '-d': "run server in debug mode",
    '-p': "user's port, next value must be corect port number"
}

if len(args) > 1:
    for flag in args[1::]:
        if flag not in allowedFlags:
            raise ValueError(f'There is not arg «{flag}» try use -help')

if '-d' in args:
    debug_mode = True
if '-p' in args:
    my_port = args[args.index('-p') + 1]
if '-help' in args:
    print('You can use flags:')
    for command in help_info.keys():
        print(f'''\t «{command}» : {help_info[command]} ''')
    exit()

app.run(host="0.0.0.0", debug=debug_mode, port=my_port)
