analytics:
	python analytics.py

news:
	python -c 'import header; header.main();'

clean:
	find . -name '*.pyc' -delete
	find . -name '*html' -delete

clean-mysql:
	python cleaner.py
	python cleaner-db.py

backup:
	sh monitor-mysql-backup.sh

backup-recover:
	mysql -uroot -pblabla6 monitor < monitor.sql

Chart:
	curl "https://raw.githubusercontent.com/nnnick/Chart.js/master/Chart.js" 1> Chart.js 2>/dev/null

chown:
	sudo find . -user root -exec chown odroid:odroid {} \;

chown-web:
	sudo find /var/www/patrickz/ -user root -exec chown odroid:odroid {} \;
	sudo find /var/www/odroid/ -user root -exec chown odroid:odroid {} \;

sigma-js:
	sudo cp -r ./sigma-js /var/www/patrickz/data
	sudo cp -r ./sigma-js /var/www/odroid/data

	sudo chown www-data:www-data /var/www/patrickz/sigma-js/*
    sudo chown www-data:www-data /var/www/odroid/sigma-js/*

web: Chart
	sudo cp monitor.php search.php search-user.php monitor-json.php Chart.js /var/www/patrickz/
	sudo cp monitor.php search.php search-user.php monitor-json.php Chart.js /var/www/odroid/

	sudo cp news.png news.ico icon.png icon-apple.png /var/www/patrickz/
	sudo cp news.png news.ico icon.png icon-apple.png /var/www/odroid/

    sudo chown www-data:www-data /var/www/patrickz/*
    sudo chown www-data:www-data /var/www/odroid/*

nohup:
	sudo nohup python web.py 1>/dev/null 2>/dev/null &
