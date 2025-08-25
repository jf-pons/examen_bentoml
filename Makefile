IMAGE_NAME=pons_student_admission

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

build:
	pipenv run bentoml build

containerize:
	pipenv run bentoml containerize ${IMAGE_NAME}:latest

test:
	image_id=$$(docker images --format '{{.Repository}}:{{.Tag}} {{.CreatedAt}} {{.ID}}' \
		| grep '^${IMAGE_NAME}:' \
		| sort -rk2 \
		| head -n1 \
		| awk '{print $$1}'); \
	if [ -n "$$image_id" ]; then \
		echo "Running Docker image: $$image_id"; \
		container_id=$$(docker run -d --rm -p 3000:3000 $$image_id); \
		echo "Waiting 2s for container to be ready..."; \
		sleep 2; \
		pipenv install --dev && \
		pipenv run python -m pytest tests; \
		echo "Stopping container $$container_id"; \
		docker stop $$container_id; \
	else \
		echo "No image found for ${IMAGE_NAME}"; \
		exit 1; \
	fi

generate_archive:
	docker save -o bento_image.tar ${IMAGE_NAME}

all: setup get_data clean_data train_model build containerize test generate_archive

clean_csv:
	rm -f data/raw/admission.csv && \
	rm -f data/processed/X_train.csv && \
	rm -f data/processed/X_test.csv && \
	rm -f data/processed/y_train.csv && \
	rm -f data/processed/y_test.csv

clean_bentoml:
	pipenv run bentoml delete ${IMAGE_NAME} -y && \
	pipenv run bentoml models delete student_admission -y

clean_docker:
	@images=$$(docker images --format '{{.Repository}}:{{.Tag}}' | grep student_admission || true); \
	if [ -n "$$images" ]; then \
		docker image rm -f $$images; \
	else \
		echo "No student_admission Docker images found."; \
	fi

clean_archive:
	rm bento_image.tar

clean:
	-$(MAKE) clean_csv
	-$(MAKE) clean_bentoml
	-$(MAKE) clean_docker
	-$(MAKE) clean_archive
	
