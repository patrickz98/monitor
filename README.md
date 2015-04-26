Install MySql:

* sudo apt-get install mysql-server

* sudo apt-get install python-mysqldb

* sudo nano /etc/mysql/my.cnf
-> bind-address= 0.0.0.0

* CREATE DATABASE monitor;

* CREATE USER 'monitor'@'%' IDENTIFIED BY 'test123';

* grant all on monitor.* to monitor;

Todo:

* search interface graph

Quellen:
* http://www.chartjs.org/docs/
* https://www.iconfinder.com/icons/115708/news_newspaper_subscribe_icon#size=128
* http://mysql-python.sourceforge.net/
* https://github.com/farcepest/MySQLdb1


Notes:

Stuff
* display:inline
* ALTER DATABASE monitor CHARACTER SET utf8 COLLATE utf8_unicode_ci;
