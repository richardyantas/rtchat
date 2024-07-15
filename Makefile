.PHONY: conda-install
conda-install:
	pip-compile app/requirements/prod.in && pip-compile app/requirements/dev.in
	pip-sync app/requirements/prod.txt app/requirements/dev.txt

.PHONY: conda-create
conda-create:
	conda env update -f environment.yml; 
# conda activate django-composer

.PHONY: conda-remove
conda-remove:
	conda env remove --name django-composer

.PHONY: install
install:
	pip install -r app/requirements/dev.txt

.PHONY: install-pre-commit
install-pre-commit:
	pip uninstall -y pre-commit; 
	pip install pre-commit;	

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: test
test:
	python app/manage.py test

.PHONY: update
update:
	install migrate install-pre-commit