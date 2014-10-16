Install MySql:

* sudo apt-get install mysql-server

* sudo apt-get install python-mysqldb

* sudo nano /etc/mysql/my.cnf
-> bind-address= 0.0.0.0

* CREATE DATABASE monitor;

* CREATE USER 'monitor'@'%' IDENTIFIED BY 'test123';

* grant all on monitor.* to monitor;

Todo:

* search interface

Quellen:
* http://www.chartjs.org/docs/
* https://www.iconfinder.com/icons/115708/news_newspaper_subscribe_icon#size=128
* http://mysql-python.sourceforge.net/
* https://github.com/farcepest/MySQLdb1


Notes:

Python webserver
* sudo apt-get install libapache2-mod-python

Conf
* AddHandler mod_python .psp
  PythonHandler mod_python.psp
  PythonDebug On

Stuff
* display:inline