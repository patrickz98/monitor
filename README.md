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

* windows compatibly

Quellen:
* http://www.chartjs.org/docs/
* https://www.iconfinder.com/icons/115708/news_newspaper_subscribe_icon#size=128
* http://mysql-python.sourceforge.net/
* https://github.com/farcepest/MySQLdb1


		<input type="image"
			src="Ello.Faces.800.gif"
			onClick="parent.location='statistik.html'"
			value='Sort'
			style="height:25px; width:75px">
		<input type=button
			onClick="parent.location='statistik.html'"
			value='Unsort'
			style="height:25px; width:75px">