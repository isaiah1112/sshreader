# Use current project version for docker image
DOCKER_TAG := $(shell git describe --tags)
# Container ID of docker image (if running)
DOCKER_CID := $(shell docker ps -a -q -f name=sshreader_test)
UV_PATH := $(shell which uv 2>/dev/null)

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo "\nTargets:"
	@echo "  install            Install this package (pip install)"
	@echo "  docs               Build Sphinx documentation"
	@echo "  test               Run unit tests (requires Docker)"
	@echo "  coverage           Build an HTML coverage report"
	@echo "  lint               Run 'ruff' linting on project"
	@echo "\nSpecial Targets:"
	@echo "  docker-build       Build ssh server image for unit/integration tests"
	@echo "  docker-push        Push ssh server image to Docker Hub"
	@echo "  test-clean         Cleans up running Docker containers"

# Install UV if not installed
.PHONY: uv-init
uv-init:
	@if [ -z "$(UV_PATH)" ]; then curl -LsSf https://astral.sh/uv/install.sh | sh; fi

.PHONY: install
install:
	@python -m pip install .

.PHONY: docker-build
docker:
	@docker build -t isaiah1112/sshreader:$(DOCKER_TAG) .
	@docker tag isaiah1112/sshreader:$(DOCKER_TAG) isaiah1112/sshreader:latest

.PHONY: docker-push
docker-push: docker-build
	@docker push --all-tags isaiah1112/sshreader

.PHONY: docs
docs: uv-init
	@uv run --group docs sphinx-build -b html docs/source/ docs/build/html/

.PHONY: test
test: test-init
	@uv run --group test coverage run -m unittest discover tests/

.PHONY: coverage
test-coverage: test
	@uv run --group test coverage html

.PHONY: lint
lint: uv-init
	@uv run --group test ruff check sshreader/

.PHONY: test-clean
test-clean:
	@if [ -n "$(DOCKER_CID)" ]; then docker stop $(DOCKER_CID) >/dev/null; docker container rm $(DOCKER_CID) >/dev/null; fi
	@echo "Stopped and Removed sshreader_test container"

.PHONY: test-init
test-init: uv-init
	@if [ -z "$(DOCKER_CID)" ]; then\
		if [ -z "$(SSH_PORT)" ]; then\
			echo "Starting sshreader_test container on port 22";\
 			docker run -d -p 127.0.0.1:22:22 --name sshreader_test isaiah1112/sshreader:latest > /dev/null;\
 		else\
 			echo "Starting sshreader_test container on port $(SSH_PORT)";\
 			docker run -d -p 127.0.0.1:$(SSH_PORT):22 --name sshreader_test isaiah1112/sshreader:latest > /dev/null;\
 		fi\
 	fi