all:
	python analytics.py
	
mysql:
	python -c 'import header; header.main();'

clean:
	find . -name '*.pyc' -delete
	find . -name '*.html' -delete

backup:
	sh monitor-mysql-backup.sh

lib:
	curl "https://raw.githubusercontent.com/nnnick/Chart.js/master/Chart.js" 1> Chart.js 2>/dev/null
