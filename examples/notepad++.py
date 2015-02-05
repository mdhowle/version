import ftplib
try:
    import winreg
except ImportError:
    import _winreg as winreg

try:
    from version import Version
except ImportError:
    import sys
    import os
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(root)
    from version import Version

def get_latest(site, directory):
    with ftplib.FTP() as ftp:
        ftp.connect(site)
        ftp.login()
        files = ftp.mlsd(directory)
        latest = Version(0.0)
        for file in files:
            if file[0] in ('.', '..'):
                continue

            if latest < file[0]:
                latest = Version(file[0])
    return latest

if __name__ == '__main__':
    reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Notepad++"
    with winreg.OpenKey(reg, key) as np:
        try:
            npver = winreg.QueryValueEx(np, "DisplayVersion")
        except FileNotFoundError:
            npver = '0.0'

    installed = Version(npver)

    latest = get_latest("download.tuxfamily.org", '/notepadplus')

    if installed < latest:
        print("A new version is available: {0}".format(latest))
    elif installed > latest:
        print("You have a higher version installed than available: {0} > {1}".format(installed, latest))
    else:
        print("You have the latest version: {0}".format(latest))
