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

train_model:
	python src/train_model.py

all: setup get_data clean_data train_model

clean:
	rm -f data/raw/admission.csv && \
	rm -f data/processed/X_train.csv && \
	rm -f data/processed/X_test.csv && \
	rm -f data/processed/y_train.csv && \
	rm -f data/processed/y_test.csv && \
	bentoml models delete student_admission -y

