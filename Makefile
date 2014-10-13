all:
	python analytics-html.py
	python analytics-html-sort.py
	python analytics-html-unsort.py

news:
	python -c 'import header; header.main();'

mysql:
	python analytics.py > /dev/null

clean:
	find . -name '*.pyc' -delete
	find . -name '*html' -delete

backup:
	sh monitor-mysql-backup.sh

lib:
	curl "https://raw.githubusercontent.com/nnnick/Chart.js/master/Chart.js" 1> Chart.js 2>/dev/null

chown:
	sudo find . -user root -exec chown odroid:odroid {} \;

web: lib all
	sudo cp Chart.js /var/www/patrickz/
	sudo cp Chart.js /var/www/odroid/

	sudo chown www-data:www-data /var/www/patrickz/Chart.js
	sudo chown www-data:www-data /var/www/odroid/Chart.js

	sudo cp news.png news.ico /var/www/patrickz/
	sudo cp news.png news.ico /var/www/odroid/

	sudo chown www-data:www-data /var/www/patrickz/news.png
	sudo chown www-data:www-data /var/www/odroid/news.png
	
	sudo chown www-data:www-data /var/www/patrickz/news.ico
	sudo chown www-data:www-data /var/www/odroid/news.ico

	sudo cp aktuell.html /var/www/patrickz/
	sudo cp aktuell.html /var/www/odroid/

	sudo chown www-data:www-data /var/www/patrickz/aktuell.html
	sudo chown www-data:www-data /var/www/odroid/aktuell.html

	sudo cp aktuell-*.html /var/www/patrickz/
	sudo cp aktuell-*.html /var/www/odroid/

	sudo chown www-data:www-data /var/www/patrickz/aktuell-*.html
	sudo chown www-data:www-data /var/www/odroid/aktuell-*.html

	sudo cp -r html /var/www/patrickz/
	sudo cp -r html /var/www/odroid/
	
	sudo chown www-data:www-data /var/www/patrickz/html/
	sudo chown www-data:www-data /var/www/odroid/html/

	sudo chown www-data:www-data /var/www/patrickz/html/*
	sudo chown www-data:www-data /var/www/odroid/html/*

nohup:
	sudo nohup python web.py 1>/dev/null 2>/dev/null &
