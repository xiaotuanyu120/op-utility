import pexpect
import os
import sys


def key_gen(host="id_rsa"):
    key_file = '/root/.ssh/'+''.join(str(host).strip())
    if os.path.isfile(key_file):
        os.system("mv %s %s.old" % (key_file, key_file))
        os.system("mv %s.pub %s.pub.old" % (key_file, key_file))
    child = pexpect.spawn('ssh-keygen -b 1024 -t rsa')
    try:
        child.expect('save the key')
        child.sendline(key_file)
 
        child.expect('passphrase')
        child.sendline('')
        child.expect('passphrase')
        child.sendline('')
 
        child.expect(pexpect.EOF)
    except:
        e = sys.exc_info()[0]
        print "KEYGEN ERROR" + e


def key_copy(host, password, id_rsa):
    copy_default = 'ssh-copy-id -i /root/.ssh/id_rsa.pub root@%s' % host
    copy_host = 'ssh-copy-id -i /root/.ssh/%s.pub root@%s' % (host, host)
    try:
        if id_rsa:
            child = pexpect.spawn(copy_default)
        else:
            child = pexpect.spawn(copy_host)
 
        index = child.expect(['yes/no', 'password'])
        if index == 0:
            child.sendline('yes')
        elif index == 1:
            print "start input password"
            child.sendline(password)
        child.expect(pexpect.EOF)
    except:
        e = sys.exc_info()[0]
        print "COPY ERROR" + e
