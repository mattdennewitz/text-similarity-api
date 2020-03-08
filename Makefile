install:
	pip install -r requirements.txt
	python -m spacy download en_core_web_lg

run:
	uvicorn api:app --reload
