echo '****************nginx install****************'
yum install gcc gcc-c++ cmake ncurses-devel -y
yum groupinstall base "Development Tools" -y

groupadd nginx
useradd -g nginx nginx

yum install -y pcre-devel openssl openssl-devel

/bin/cp ./nginxd /etc/init.d/
chmod 755 /etc/init.d/nginxd
chkconfig nginxd on

/bin/cp ./nginx-1.8.0.tar.gz /usr/local/
cd /usr/local
tar zxvf nginx-1.8.0.tar.gz

cd nginx-1.8.0
./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module --with-pcre --with-http_realip_module
make
make install

service nginxd start

mkdir -p /data/web
mkdir -p /data/web/www
mkdir -p /data/web/log
mkdir /web
ln -s /data/web/www /web/www
ln -s /data/web/log /web/log
echo "export PATH=$PATH:/usr/local/nginx/sbin:/usr/local/mysql/bin:/usr/local/php/bin" >> /etc/profile
. /etc/profile
echo "****************INSTALL FINISH*****************"