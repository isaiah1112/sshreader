.PHONY: docker-build docker-push docs install test test-clean test-coverage test-init

DOCKER_TAG = $(shell git describe)
DOCKER_CID = $(shell docker ps -q -f name=sshreader_test)

docker:
	@docker build -t isaiah1112/sshreader:$(DOCKER_TAG) .
	@docker tag isaiah1112/sshreader:$(DOCKER_TAG) isaiah1112/sshreader:latest

docker-push: docker
	@docker push --all-tags isaiah1112/sshreader

docs:
	@python -m pip install Sphinx
	@sphinx-build -b html docs/source/ docs/build/html/

install:
	@python -m pip install -U -e .

test: test-init
	@coverage run -m unittest discover tests/

test-clean:
	@if [ -n "$(DOCKER_CID)" ]; then docker stop $(DOCKER_CID) >/dev/null; docker container rm $(DOCKER_CID) >/dev/null; fi
	@echo "Stopped and Removed sshreader_test container"

test-coverage: test
	@coverage html

test-init:
	@python -m pip install -U -r requirements.txt
	@if [ -z "$(DOCKER_CID)" ]; then\
		if [ -z "$(SSH_PORT)" ]; then\
			echo "Starting sshreader_test container on port 22";\
 			docker run -d -p 127.0.0.1:22:22 --name sshreader_test isaiah1112/sshreader:latest > /dev/null;\
 		else\
 			echo "Starting sshreader_test container on port $(SSH_PORT)";\
 			docker run -d -p 127.0.0.1:$(SSH_PORT):22 --name sshreader_test isaiah1112/sshreader:latest > /dev/null;\
 		fi\
 	fi
