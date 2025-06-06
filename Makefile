DOCKER_TAG := $(shell git describe --tags)
DOCKER_CID := $(shell docker ps -a -q -f name=sshreader_test)
UV_PATH := $(shell which uv 2>/dev/null)

.PHONY: init
init:
	@if [ -z "$(UV_PATH)" ]; then curl -LsSf https://astral.sh/uv/install.sh | sh; fi

.PHONY: docker
docker:
	@docker build -t isaiah1112/sshreader:$(DOCKER_TAG) .
	@docker tag isaiah1112/sshreader:$(DOCKER_TAG) isaiah1112/sshreader:latest

.PHONY: docker-push
docker-push: docker
	@docker push --all-tags isaiah1112/sshreader

.PHONY: docs
docs: init
	@uv run --group docs sphinx-build -b html docs/source/ docs/build/html/

.PHONY: test
test: test-init
	@uv run --group dev coverage run -m unittest discover tests/

.PHONY: test-clean
test-clean:
	@if [ -n "$(DOCKER_CID)" ]; then docker stop $(DOCKER_CID) >/dev/null; docker container rm $(DOCKER_CID) >/dev/null; fi
	@echo "Stopped and Removed sshreader_test container"

.PHONY: test-coverage
test-coverage: test
	@uv run --group dev coverage html

.PHONY: test-init
test-init: init
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
	@uv run --group dev ruff check sshreader/