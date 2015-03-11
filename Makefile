all:
	python analytics-html.py
	python week-word-html.py
	python week-data-html.py

news:
	python -c 'import header; header.main();'

mysql:
	python analytics.py > /dev/null
	python cleaner.py
	python cleaner-db.py

clean:
	find . -name '*.pyc' -delete
	find . -name '*html' -delete

search:
	sudo cp search.php /var/www/odroid/
	sudo cp search.php /var/www/patrickz/
	
	sudo chown www-data:www-data /var/www/patrickz/search.php
	sudo chown www-data:www-data /var/www/odroid/search.php
	
backup:
	sh monitor-mysql-backup.sh

archiv: backup
	mysql -uroot -pblabla6 monitorbig < monitor.sql
	
lib:
	curl "https://raw.githubusercontent.com/nnnick/Chart.js/master/Chart.js" 1> Chart.js 2>/dev/null

chown:
	sudo find . -user root -exec chown odroid:odroid {} \;

week:	
	sudo cp week-word.html week-data.html /var/www/patrickz/
	sudo cp week-word.html week-data.html /var/www/odroid/
	
	sudo chown www-data:www-data /var/www/patrickz/week-word.html
	sudo chown www-data:www-data /var/www/odroid/week-word.html

	sudo chown www-data:www-data /var/www/patrickz/week-data.html
	sudo chown www-data:www-data /var/www/odroid/week-data.html

web: chown lib all week
    sudo cp monitor.php /var/www/patrickz/
    sudo cp monitor.php /var/www/odroid/

    sudo chown www-data:www-data /var/www/patrickz/monitor.php
    sudo chown www-data:www-data /var/www/odroid/monitor.php

	sudo cp Chart.js /var/www/patrickz/
	sudo cp Chart.js /var/www/odroid/

	sudo chown www-data:www-data /var/www/patrickz/Chart.js
	sudo chown www-data:www-data /var/www/odroid/Chart.js

	sudo cp news.png news.ico icon.png /var/www/patrickz/
	sudo cp news.png news.ico icon.png /var/www/odroid/

	sudo chown www-data:www-data /var/www/patrickz/news.png
	sudo chown www-data:www-data /var/www/odroid/news.png
	
	sudo chown www-data:www-data /var/www/patrickz/news.ico
	sudo chown www-data:www-data /var/www/odroid/news.ico

    sudo chown www-data:www-data /var/www/patrickz/icon.png
    sudo chown www-data:www-data /var/www/odroid/icon.png

	sudo cp aktuell.html /var/www/patrickz/
	sudo cp aktuell.html /var/www/odroid/

	sudo chown www-data:www-data /var/www/patrickz/aktuell.html
	sudo chown www-data:www-data /var/www/odroid/aktuell.html

	sudo cp -r html /var/www/patrickz/
	sudo cp -r html /var/www/odroid/
	
	sudo chown www-data:www-data /var/www/patrickz/html/
	sudo chown www-data:www-data /var/www/odroid/html/

	sudo chown www-data:www-data /var/www/patrickz/html/*
	sudo chown www-data:www-data /var/www/odroid/html/*

nohup:
	sudo nohup python web.py 1>/dev/null 2>/dev/null &
