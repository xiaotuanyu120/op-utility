from fabric.api import local
from fabric.api import env
from fabric.api import runs_once

from keygen_ssh import key_gen
from keygen_ssh import key_copy

hosts = {
        '172.16.2.3': 'Sudoroot88',
}

env.hosts = [x for x in hosts]

env.passwords = {'root@'+x+':22': hosts[x] for x in hosts}

@runs_once
def ssh_key_gen():
    for host in hosts:
        key_gen(host)

@runs_once
def ssh_key_copy():
    for host in hosts:
        key_copy(host, hosts[host])
