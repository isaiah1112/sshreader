DOCKER_TAG := $(shell git describe --tags)
DOCKER_CID := $(shell docker ps -q -f name=sshreader_test)

.PHONY: docker
docker:
	@docker build -t isaiah1112/sshreader:$(DOCKER_TAG) .
	@docker tag isaiah1112/sshreader:$(DOCKER_TAG) isaiah1112/sshreader:latest

.PHONY: docker-push
docker-push: docker
	@docker push --all-tags isaiah1112/sshreader

.PHONY: docs
docs:
	@python -m pip install Sphinx
	@sphinx-build -b html docs/source/ docs/build/html/

.PHONY: install
install:
	@python -m pip install -U .

.PHONY: install-dev
install-dev:
	@python -m pip install -U -e .

.PHONY: test
test: test-init
	@coverage run -m unittest discover tests/

.PHONY: test-clean
test-clean:
	@if [ -n "$(DOCKER_CID)" ]; then docker stop $(DOCKER_CID) >/dev/null; docker container rm $(DOCKER_CID) >/dev/null; fi
	@echo "Stopped and Removed sshreader_test container"

.PHONY: test-coverage
test-coverage: test
	@coverage html

.PHONY: test-init
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

.PHONY: test-lint
test-lint:
	@python -m pip install -U -r requirements.txt
	@flake8 sshreader/ --count --select=E9,F63,F7,F82 --show-source --statistics --exclude docs
	@flake8 sshreader/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude docs