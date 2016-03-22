import pexpect
import sys
import os
import datetime

def key_gen(host):
    key_file = '/root/.ssh/'+''.join(str(host).strip())
    if os.path.isfile(key_file):
        os.system("mv %s %s.old" % (key_file, key_file))
    #    key_file = key_file+"-"+datetime.datetime.now().strftime("%Y-%m-%d")
    child = pexpect.spawn('ssh-keygen -b 1024 -t rsa')
    fout = file('key_gen.log', 'w')
    child.logfile = fout

    child.expect('save the key')
    child.sendline(key_file)

    child.expect('passphrase')
    child.sendline('')
    child.expect('passphrase')
    child.sendline('')

    child.expect(pexpect.EOF)

def key_copy(host, password):
    child = pexpect.spawn('ssh-copy-id -i /root/.ssh/%s.pub root@%s' % (host,
    host))
    
    index = child.expect(['yes/no', 'password'])
    if index == 0:
        child.sendline('yes')
    elif index == 1:
        child.sendline(password)
    child.expect(pexpect.EOF)
