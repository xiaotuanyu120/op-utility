echo 'mysql install'
yum install gcc gcc-c++ cmake ncurses-devel -y
yum groupinstall base "Development Tools" -y

groupadd mysql
useradd -r -g mysql mysql

mkdir -p /data/server
cd /usr/local/src
wget http://cdn.mysql.com/archives/mysql-5.1/mysql-5.1.72.tar.gz
tar zxvf mysql-5.1.72.tar.gz
cd mysql-5.1.72
./configure --prefix=/data/server/mysql --with-mysqld-user=mysql
--with-charset=utf8 --with-extra-charsets=all
make
make install

mkdir /data/mysql-data
chown -R mysql:mysql /data/server/mysql/
chown -R mysql:mysql /data/mysql-data/

./scripts/mysql_install_db --datadir=/data/mysql-data/
--basedir=/data/server/mysql/ --user=mysql
cp ./support-files/mysql.server /etc/init.d/mysqld
mv /etc/my.cnf /etc/my.cnf.old
cp support-files/my-medium.cnf /etc/my.cnf
chmod 755 /etc/init.d/mysqld

sed -inr 's#^basedir=#basedir=/data/server/mysql#g' /etc/init.d/mysqld
sed -inr 's#^datadir=#datadir=/data/mysql-data#g' /etc/init.d/mysqld
ln -s /data/server/mysql /usr/local/mysql

chkconfig mysqld on
/etc/init.d/mysqld start
/data/server/mysql/bin/mysqladmin -u root password 'igamemysql'

echo 'php install'
useradd -r -s /sbin/nologin php-fpm
yum install libxml2-devel libcurl-devel libjpeg-turbo-devel libpng-devel freetype-devel libmcrypt-devel epel-release libevent-devel -y
ln -s /usr/lib64/libjpeg.so /usr/lib/libjpeg.so 
ln -s /usr/lib64/libpng.so /usr/lib/libpng.so
cd /usr/local/src
wget http://museum.php.net/php5/php-5.3.3.tar.gz
tar zxvf php-5.3.3.tar.gz
cd php-5.3.3
./configure --prefix=/data/server/php
--with-config-file-path=/data/server/php/etc --enable-fpm
--with-fpm-user=php-fpm --with-fpm-group=php-fpm
--with-mysql=/data/server/mysql --with-mysql-sock=/tmp/mysql.sock
--with-libxml-dir  --with-gd --with-jpeg-dir --with-png-dir --with-freetype-dir
--with-iconv-dir --with-zlib-dir --with-mcrypt --enable-soap
--enable-gd-native-ttf --enable-ftp --enable-mbstring --enable-exif
--disable-ipv6 --with-curl
make
make install

mkdir /data/server/php/etc
cp php.ini-production /data/server/php/etc/php.ini
cp /data/server/php/etc/php-fpm.conf.default /data/server/php/etc/php-fpm.conf
cp ./sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm
chmod 755 /etc/init.d/php-fpm
mkdir /etc/php
ln -s /data/server/php /usr/local/php
chkconfig --add php-fpm
chkconfig php-fpm on
sed -inr 's/.*pm.start_servers = 20.*/pm.start_servers = 20/g'
/data/server/php/etc/php-fpm.conf
sed -inr 's/.*pm.min_spare_servers = 5.*/pm.min_spare_servers = 5/g'
/data/server/php/etc/php-fpm.conf
sed -inr 's/.*pm.max_spare_servers = 35.*/pm.max_spare_servers = 35/g'
/data/server/php/etc/php-fpm.conf
sed -inr 's#.*pid = /data/server/php/var/run/php-fpm.pid.*#pid = /data/server/php/var/run/php-fpm.pid#g' /data/server/php/etc/php-fpm.conf



echo 'nginx install'
groupadd nginx
useradd -g nginx nginx
yum install -y pcre-devel openssl openssl-devel
cd /usr/local/src
wget http://nginx.org/download/nginx-1.8.0.tar.gz
tar zxvf nginx-1.8.0.tar.gz
cd nginx-1.8.0
./configure --user=nginx --group=nginx --prefix=/data/server/nginx --with-http_stub_status_module --with-http_ssl_module --with-pcre --with-http_realip_module
make
make install
echo 'autorun daemon'
echo '#!/bin/bash' > /etc/init.d/nginxd
echo '# chkconfig: - 30 21' >> /etc/init.d/nginxd
echo '# description: http service.' >> /etc/init.d/nginxd
echo '' >> /etc/init.d/nginxd
echo '# Source Function Library' >> /etc/init.d/nginxd
echo '. /etc/init.d/functions' >> /etc/init.d/nginxd
echo '' >> /etc/init.d/nginxd
echo '# Nginx Settings' >> /etc/init.d/nginxd
echo 'NGINX_SBIN="/data/server/nginx/sbin/nginx"' >> /etc/init.d/nginxd
echo 'NGINX_CONF="/data/server/nginx/conf/nginx.conf"' >> /etc/init.d/nginxd
echo 'NGINX_PID="/data/server/nginx/logs/nginx.pid"' >> /etc/init.d/nginxd
echo 'RETVAL=0' >> /etc/init.d/nginxd
echo 'prog="Nginx"' >> /etc/init.d/nginxd
echo '' >> /etc/init.d/nginxd
echo 'start() {' >> /etc/init.d/nginxd
echo '         echo -n $"Starting $prog: "' >> /etc/init.d/nginxd
echo '         mkdir -p /dev/shm/nginx_temp' >> /etc/init.d/nginxd
echo '         daemon $NGINX_SBIN -c $NGINX_CONF' >> /etc/init.d/nginxd
echo '         RETVAL=$?' >> /etc/init.d/nginxd
echo '         echo' >> /etc/init.d/nginxd
echo '         return $RETVAL' >> /etc/init.d/nginxd
echo '}' >> /etc/init.d/nginxd
echo '' >> /etc/init.d/nginxd
echo 'stop() {' >> /etc/init.d/nginxd
echo '         echo -n $"Stopping $prog: "' >> /etc/init.d/nginxd
echo '         killproc -p $NGINX_PID $NGINX_SBIN -TERM' >> /etc/init.d/nginxd
echo '         rm -rf /dev/shm/nginx_temp' >> /etc/init.d/nginxd
echo '         RETVAL=$?' >> /etc/init.d/nginxd
echo '         echo' >> /etc/init.d/nginxd
echo '         return $RETVAL' >> /etc/init.d/nginxd
echo '}' >> /etc/init.d/nginxd
echo '' >> /etc/init.d/nginxd
echo 'reload(){' >> /etc/init.d/nginxd
echo '         echo -n $"Reloading $prog: "' >> /etc/init.d/nginxd
echo '         killproc -p $NGINX_PID $NGINX_SBIN -HUP' >> /etc/init.d/nginxd
echo '         RETVAL=$?' >> /etc/init.d/nginxd
echo '         echo' >> /etc/init.d/nginxd
echo '         return $RETVAL' >> /etc/init.d/nginxd
echo '}' >> /etc/init.d/nginxd
echo '' >> /etc/init.d/nginxd
echo 'restart(){' >> /etc/init.d/nginxd
echo '         stop' >> /etc/init.d/nginxd
echo '         start' >> /etc/init.d/nginxd
echo '}' >> /etc/init.d/nginxd
echo '' >> /etc/init.d/nginxd
echo 'configtest(){' >> /etc/init.d/nginxd
echo '     $NGINX_SBIN -c $NGINX_CONF -t' >> /etc/init.d/nginxd
echo '     return 0' >> /etc/init.d/nginxd
echo '}' >> /etc/init.d/nginxd
echo 'case "$1" in' >> /etc/init.d/nginxd
echo '   start)' >> /etc/init.d/nginxd
echo '         start' >> /etc/init.d/nginxd
echo '         ;;' >> /etc/init.d/nginxd
echo '   stop)' >> /etc/init.d/nginxd
echo '         stop' >> /etc/init.d/nginxd
echo '         ;;' >> /etc/init.d/nginxd
echo '   reload)' >> /etc/init.d/nginxd
echo '         reload' >> /etc/init.d/nginxd
echo '         ;;' >> /etc/init.d/nginxd
echo '   restart)' >> /etc/init.d/nginxd
echo '         restart' >> /etc/init.d/nginxd
echo '         ;;' >> /etc/init.d/nginxd
echo '   configtest)' >> /etc/init.d/nginxd
echo '         configtest' >> /etc/init.d/nginxd
echo '         ;;' >> /etc/init.d/nginxd
echo '   *)' >> /etc/init.d/nginxd
echo '         echo $"Usage: $0 {start|stop|reload|restart|configtest}"' >> /etc/init.d/nginxd
echo '         RETVAL=1' >> /etc/init.d/nginxd
echo 'esac' >> /etc/init.d/nginxd
echo 'exit $RETVAL' >> /etc/init.d/nginxd

ln -s /data/server/nginx /usr/local/nginx

chmod 755 /etc/init.d/nginxd
chkconfig nginxd on
service nginxd start

mkdir /data/web
mkdir /data/web/www
mkdir /data/web/log
mkdir /web
ln -s /data/web/www /web/www
ln -s /data/web/log /web/log
echo "export PATH=$PATH:/data/server/nginx/sbin:/data/server/mysql/bin:/data/server/php/bin" >> /etc/profile
. /etc/profile
