get_data:
	cd data/raw && \
	wget https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv -O admission.csv && \
	cd ../.. \

setup:
	pipenv install

clean_data:
	pipenv run python -m src.prepare_data

train_model:
	pipenv run python -m src.train_model

serve_model:
	pipenv run bentoml serve src.service:StudentAdmissionService --reload &

all: setup get_data clean_data train_model 

test:
	pipenv install --dev && \
	pipenv run python -m pytest tests

clean:
	kill -9 $(lsof -t -i:3000 -sTCP:LISTEN -a -c python) && \
	rm -f data/raw/admission.csv && \
	rm -f data/processed/X_train.csv && \
	rm -f data/processed/X_test.csv && \
	rm -f data/processed/y_train.csv && \
	rm -f data/processed/y_test.csv && \
	bentoml models delete student_admission -y

