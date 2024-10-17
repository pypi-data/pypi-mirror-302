SHELL:=/bin/bash

build: dist

dist:
	python3 -m pip install --upgrade build
	python3 -m build

clean:
	rm -rf dist

publish-test: dist
	python3 -m pip install --upgrade twine
	@echo =====================
	@echo INSTRUCTIONS:
	@echo - API token: see https://test.pypi.org/manage/account/token/
	@echo =====================
	python3 -m twine upload --repository testpypi --verbose $</*

publish: dist
	@echo "Please type 'confirm' to publish package to pypi: "; \
	read confirmation; \
	echo $$confirmation; \
	if [[ "$$confirmation" != "confirm" ]]; then \
		exit 1; \
	fi

	python3 -m pip install --upgrade twine
	@echo =====================
	@echo INSTRUCTIONS:
	@echo - API token: see https://pypi.org/manage/account/token/
	@echo =====================
	python3 -m twine upload --verbose $</*
