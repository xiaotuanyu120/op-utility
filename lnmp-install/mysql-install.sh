## env setting
BASEDIR=/usr/local/mysql
DATADIR=/data/mysql-data
PASSWORD=igamemysql

## mysql base env install
yum install gcc gcc-c++ cmake ncurses-devel -y
yum groupinstall base "Development Tools" -y

## create user
groupadd mysql
useradd -r -g mysql mysql

## source package unzip
[[ -d mysql ]] || mkdir mysql && mv mysql /tmp && tmp_mv=1
tar zxvf mysql-5.1.72.tar.gz -C mysql
cd mysql

## mysql install
./configure --prefix=$BASEDIR --datadir=$DATADIR --with-mysqld-user=mysql --with-charset=utf8 --with-extra-charsets=all
make
make install

mkdir -p $DATADIR
chown -R mysql:mysql $BASEDIR
chown -R mysql:mysql $DATADIR

## mysql initial
./scripts/mysql_install_db --datadir=$DATADIR --basedir=$BASEDIR --user=mysql
cp ./support-files/mysql.server /etc/init.d/mysqld
mv /etc/my.cnf /etc/my.cnf.old
cp support-files/my-medium.cnf /etc/my.cnf
chmod 755 /etc/init.d/mysqld

sed -inr "s#^basedir=#basedir=$(BASEDIR)#g" /etc/init.d/mysqld
sed -inr "s#^datadir=#datadir=$(DATADIR)#g" /etc/init.d/mysqld

## service start and enanble
chkconfig mysqld on
/etc/init.d/mysqld start
/usr/local/mysql/bin/mysqladmin -u root password "$(PASSWORD)"

echo "export PATH=$PATH:$(BASEDIR)/bin" >> /etc/profile
. /etc/profile

## copy file moved to tmp back
[[ tmp_mv ]] && mv ./mysql /tmp/mysql_source && mv /tmp/mysql .
