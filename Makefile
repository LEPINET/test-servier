.PHONY: requirements
requirements:
	pip install -r requirements.txt

test:
	PYTHONPATH=`pwd` pytest -s -vv tests/

run:
	PYTHONPATH=. python3 ./run.py