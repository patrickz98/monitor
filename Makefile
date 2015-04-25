analytics:
	python analytics-html.py

news:
	python -c 'import header; header.main();'

mysql:
	python analytics.py > /dev/null
	python cleaner.py
	python cleaner-db.py

clean:
	find . -name '*.pyc' -delete
	find . -name '*html' -delete

clean-web:
	sudo rm -rf /var/www/odroid/html
	sudo rm -rf /var/www/patrickz/html

search:
	sudo cp search.php /var/www/odroid/
	sudo cp search.php /var/www/patrickz/
	
	sudo chown www-data:www-data /var/www/patrickz/search.php
	sudo chown www-data:www-data /var/www/odroid/search.php
	
backup:
	sh monitor-mysql-backup.sh

archiv: backup
	mysql -uroot -pblabla6 monitorbig < monitor.sql

Chart:
	curl "https://raw.githubusercontent.com/nnnick/Chart.js/master/Chart.js" 1> Chart.js 2>/dev/null

chown:
	sudo find . -user root -exec chown odroid:odroid {} \;

week:
	python week-word-html.py
	python week-data-html.py

	sudo cp week-word.html week-data.html /var/www/patrickz/
	sudo cp week-word.html week-data.html /var/www/odroid/
	
	sudo chown www-data:www-data /var/www/patrickz/week-word.html
	sudo chown www-data:www-data /var/www/odroid/week-word.html

web: Chart
	sudo cp monitor.php search.php Chart.js /var/www/patrickz/
	sudo cp monitor.php search.php Chart.js /var/www/odroid/

	sudo cp news.png news.ico icon.png icon-apple.png /var/www/patrickz/
	sudo cp news.png news.ico icon.png icon-apple.png /var/www/odroid/

    sudo chown www-data:www-data /var/www/patrickz/*
    sudo chown www-data:www-data /var/www/odroid/*

nohup:
	sudo nohup python web.py 1>/dev/null 2>/dev/null &
