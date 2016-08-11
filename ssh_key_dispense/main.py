import os
import getpass

from fabric.api import env
from fabric.api import runs_once

from keygen_ssh import key_gen as _key_gen
from keygen_ssh import key_copy as _key_copy

hosts = {
        '10.10.180.11': 'passwd',
        '10.10.180.4': 'passwd',
        '10.10.180.6': 'passwd',
}

env.hosts = [x for x in hosts]

env.passwords = {'root@'+x+':22': hosts[x] for x in hosts}


@runs_once
def ssh_key_gen():
    for host in hosts:
        _key_gen(host)


@runs_once
def ssh_key_gen_rsa():
    _key_gen()


@runs_once
def ssh_key_copy(id_rsa=0):
    user = getpass.getuser()
    configfile = '/%s/.ssh/config' % user
    for host in hosts:
        _key_copy(host, hosts[host], id_rsa)
        _ssh_config(configfile, host)


def _ssh_config(configfile, host):
    hostconfig = 'Host %s\nHostName %s\nIdentityfile ~/.ssh/%s\n\n'
    if not os.path.isfile(configfile):
        os.system("touch %s" % configfile)
        with open(configfile, 'a') as f:
            f.write(hostconfig % (host, host, host))
    else:
        with open(configfile, 'r') as fr:
            if 'Host '+host+'\n' in fr.readlines():
                print "exist!"
            else:
                with open(configfile, 'a') as f:
                    f.write(hostconfig % (host, host, host))


@runs_once
def ssh_key_copy_rsa(id_rsa=1):
    for host in hosts:
        _key_copy(host, hosts[host], id_rsa)
