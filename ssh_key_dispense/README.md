# ssh_key_dispense

# 使用方法
0、环境准备
    linux安装ssh工具
    python安装fabric包

1、wget keygen_ssh.py和main.py到本地目录

2、配置main.py，将需要生成key的host及其密码写进hosts={host: password, ...}

3、fab -f main.py -l
    Available commands:
        
        ssh_key_copy:拷贝key到相应host
        ssh_key_gen: 在/root/.ssh/下生成相应host的key，key为"host"&"host.pub"

4、连接方法

    ssh -i /root/.ssh/host root@host

others:

    如果host对应的key存在，keygen_ssh.py会将老key文件更名为"host.old"&"host.pub.old"
    
    如果不希望每次连接都指定-i key文件，可以在~/.ssh/config中做配置，详情请查看官网
