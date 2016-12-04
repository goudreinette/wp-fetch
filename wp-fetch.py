from ftputil import FTPHost
from os      import mkdir, chdir, path

excluded = ["wp-content"]

def clonefiles(host, user, password, site):
    ftpstring = 'ftp.' + host
    siteroot = 'domains/{host}/public_html/'.format(host=host)
    with FTPHost(ftpstring, user, password) as host:
        host.chdir(siteroot)
        getdir(host, site)

def getfile(host, path):
    print("File:", path)
    host.download(path, path)

def getdir(host, dir):
    print("Dir: ", dir)
    mkdir(dir)
    for name in host.listdir(dir):
        full = path.join(dir, name)
        if not name in excluded:
            if host.path.isfile(full):
                getfile(host, full)
            else:
                getdir(host, full)

def editconfig(dir):
    with open(dir + '/wp-config.php', 'r') as config:
        lines = config.readlines()
        config.close()
    with open(dir + '/wp-config.php', 'w') as config:
        lines.insert(80, "define('RELOCATE', true);\n")
        config.write(''.join(lines))


def main():
    clonefiles('hansvanderwoerd.eu', 'pfed180567', 'lw0OO5f323', 'test')
    editconfig('test')
