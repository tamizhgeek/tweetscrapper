from fabric.api import *

env.hosts = ['tgtesting@ssh.alwaysdata.com']

def publish():
    local('hg push')
    with cd('tweetscrapper'):

        run('hg pull')
        run('hg up')
        run('hg archive ../www/tweetscrapper')

