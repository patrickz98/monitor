all:
	python analytics.py
	
mysql:
	python -c 'import header; header.main()'

clean:
	find . -name '*.pyc' -delete