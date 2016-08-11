# ssh_key_dispense

# 使用方法
0、环境准备
    
    linux安装ssh工具
    
    python安装fabric包

1、wget keygen_ssh.py和main.py到本地目录

2、配置main.py，将需要生成key的host及其密码写进hosts={host: password, ...}

3、fab -f main.py -l
    
    Available commands:
        
        ssh_key_copy:     拷贝以host命名的key到相应host，并创建~/.ssh/config文件
        ssh_key_copy_rsa: 拷贝默认的id_rsa的key到所有的host
        ssh_key_gen:      在/root/.ssh/下生成相应host的key，key为"host"&"host.pub"
        ssh_key_gen_rsa:  在/root/.ssh/下生成默认id_rsa id_rsa.pub

4、连接方法
    ## 因为已经配置过~/.ssh/config，所以直接执行下面命令即可
    ssh host

others:

    如果host对应的key存在，keygen_ssh.py会将老key文件更名为"host.old"&"host.pub.old"
