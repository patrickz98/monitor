all:
	python analytics-html.py

mysql:
	python -c 'import header; header.main();'

clean:
	find . -name '*.pyc' -delete
	find . -name '*.html' -delete

backup:
	sh monitor-mysql-backup.sh

lib:
	curl "https://raw.githubusercontent.com/nnnick/Chart.js/master/Chart.js" 1> Chart.js 2>/dev/null

web: lib mysql all
	sudo cp Chart.js /var/www/patrickz/
	sudo cp Chart.js /var/www/odroid/

	sudo chown www-data:www-data /var/www/patrickz/Chart.js
	sudo chown www-data:www-data /var/www/odroid/Chart.js

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
