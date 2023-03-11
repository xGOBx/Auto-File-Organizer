import sys
import ctypes
import subprocess
import os

def run_as_admin(argv=None, debug=False):
    shell32 = ctypes.windll.shell32
    if argv is None and shell32.IsUserAnAdmin():
        return True

    if argv is None:
        argv = sys.argv
    if hasattr(sys, '_MEIPASS'):
        # Support pyinstaller wrapped program
        arguments = list(map(str, argv[1:]))
    else:
        arguments = list(map(str, argv))
    argument_line = u' '.join(arguments)
    executable = str(sys.executable)
    if debug:
        print('Command line: ', executable, argument_line)

    # Launch new instance with elevated privileges
    ret = shell32.ShellExecuteW(None, u"runas", executable, argument_line, None, 1)
    if int(ret) <= 32:
        return False

    # Exit current instance
    sys.exit()

if __name__ == '__main__':
    ret = run_as_admin()
    if ret is True:
        print('I have admin privilege.')
        input('Press ENTER to continue.')
    elif ret is None:
        print('I am elevating to admin privilege.')
        input('Press ENTER to exit.')
    else:
        print('Error')
