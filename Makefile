setup:
	pip install -r requirements.txt

test:
	pytest tests

run-api:
	uvicorn analytics_api.main:app --reload

run-dagster:
	dagster dev -f dagster_pipeline/repository.py

dbt-build:
	cd ShippingData && dbt build

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type f -name '*.pyc' -delete
