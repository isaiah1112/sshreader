DOCKER_TAG := $(shell git describe --tags)
DOCKER_CID := $(shell docker ps -a -q -f name=sshreader_test)
POETRY := $(shell which poetry 2>/dev/null)

.PHONY: init
init:
	@if [ -z "$(POETRY)" ]; then echo "Please install 'poetry'"; exit 1; fi

.PHONY: docker
docker:
	@docker build -t isaiah1112/sshreader:$(DOCKER_TAG) .
	@docker tag isaiah1112/sshreader:$(DOCKER_TAG) isaiah1112/sshreader:latest

.PHONY: docker-push
docker-push: docker
	@docker push --all-tags isaiah1112/sshreader

.PHONY: docs
docs: init
	@$(POETRY) install --with docs
	@$(POETRY) export -f requirements.txt --output docs/requirements.txt
	@$(POETRY) run sphinx-build -b html docs/source/ docs/build/html/

.PHONY: test
test: test-init
	@$(POETRY) run coverage run -m unittest discover tests/

.PHONY: test-clean
test-clean:
	@if [ -n "$(DOCKER_CID)" ]; then docker stop $(DOCKER_CID) >/dev/null; docker container rm $(DOCKER_CID) >/dev/null; fi
	@echo "Stopped and Removed sshreader_test container"

.PHONY: test-coverage
test-coverage: test
	@$(POETRY) run coverage html

.PHONY: test-init
test-init: init
	@$(POETRY) install --with dev
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
test-lint: init
	@$(POETRY) install --with dev
	@$(POETRY) run flake8 sshreader/ --count --select=E9,F63,F7,F82 --show-source --statistics --exclude docs
	@$(POETRY) run flake8 sshreader/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude docs