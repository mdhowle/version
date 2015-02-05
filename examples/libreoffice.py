import urllib
import urllib.request
from html.parser import HTMLParser
import winreg

try:
    from version import Version
except ImportError:
    import sys
    import os
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(root)
    from version import Version


class LinkParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.first_row = True
        self.in_cell = False
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tr' and self.first_row:
            self.first_row = False
            return
        if tag == 'td':
            self.in_cell = True
            return

        if tag == 'a' and self.in_cell:
            for attr, val in attrs:
                if attr == 'href':
                    self.links.append(val.replace('/', ''))

    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_cell = False


def get_latest_version(site):
    data = urllib.request.urlopen(site)
    p = LinkParser()
    p.feed(data.read().decode('utf-8'))

    latest = Version('0.0')
    for link in p.links:
        ver = Version(link)
        if latest < ver:
            latest = ver
    return latest


if __name__ == '__main__':
    reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{8BEE1CDD-F95D-4759-952D-6B38DF99D1F0}"

    with winreg.OpenKey(reg, key, access=winreg.KEY_READ | winreg.KEY_WOW64_32KEY) as lo:
        try:
            lover = winreg.QueryValueEx(lo, "DisplayVersion")[0][:-2] # Remove out last part of version
        except FileNotFoundError:
            lover = '0.0'

    installed_version = Version(lover)

    latest_version = get_latest_version("http://download.documentfoundation.org/libreoffice/stable/")

    if installed_version < latest_version:
        print("A new version is available: {0}".format(latest_version))
    elif installed_version > latest_version:
        print("You have a higher version installed than available: {0} > {1}".format(installed_version, latest_version))
    else:
        print("You have the latest version: {0}".format(latest_version))