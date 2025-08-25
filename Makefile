VIRTUAL_ENV="venv"

get_data:
	cd data/raw && \
	wget https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv -O admission.csv && \
	cd ../.. \

setup:
	virtualenv ${VIRTUAL_ENV} && \
	source ${VIRTUAL_ENV}/bin/activate && \
	pip install -r requirements.txt

clean_data:
	python src/prepare_data.py

all: setup get_data 