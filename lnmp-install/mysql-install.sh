echo 'mysql base env install'
yum install gcc gcc-c++ cmake ncurses-devel -y
yum groupinstall base "Development Tools" -y

echo 'create user'
groupadd mysql
useradd -r -g mysql mysql

echo 'source package download'
cd /usr/local/src
wget http://cdn.mysql.com/archives/mysql-5.1/mysql-5.1.72.tar.gz
tar zxvf mysql-5.1.72.tar.gz
cd mysql-5.1.72

echo 'mysql install'
./configure --prefix=/usr/local/mysql --with-mysqld-user=mysql --with-charset=utf8 --with-extra-charsets=all
make
make install

mkdir -p /data/mysql-data
chown -R mysql:mysql /usr/local/mysql/
chown -R mysql:mysql /data/mysql-data/

echo 'mysql initial'
./scripts/mysql_install_db --datadir=/data/mysql-data/ --basedir=/usr/local/mysql/ --user=mysql
cp ./support-files/mysql.server /etc/init.d/mysqld
mv /etc/my.cnf /etc/my.cnf.old
cp support-files/my-medium.cnf /etc/my.cnf
chmod 755 /etc/init.d/mysqld

sed -inr 's#^basedir=#basedir=/usr/local/mysql#g' /etc/init.d/mysqld
sed -inr 's#^datadir=#datadir=/data/mysql-data#g' /etc/init.d/mysqld

chkconfig mysqld on
/etc/init.d/mysqld start
/usr/local/mysql/bin/mysqladmin -u root password 'igamemysql'

echo "export PATH=$PATH:/usr/local/mysql/bin" >> /etc/profile
. /etc/profile
