
install:
	# python3 -m venv venv
	source venv/bin/activate
	pip install --upgrade pip
	pip install app/requirements.txt
lint:
	# pep8
	python manage.py pylint 
test:
	python manage.py test