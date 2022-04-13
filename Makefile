.PHONY: docker docker-push test test-clean test-init

DOCKER_TAG = $(shell git describe)
TOX_ENV = $(shell grep -o 'py[0-9]+' $(PWD)/tox.ini | tail -1)

docker:
	@docker build -t isaiah1112/sshreader:$(DOCKER_TAG) .
	@docker tag isaiah1112/sshreader:$(DOCKER_TAG) isaiah1112/sshreader:latest

docker-push: docker
	@docker push --all-tags isaiah1112/sshreader

test-init:
	@pip install -r virtualenv tox

test-clean:
	@rm $(PWD)/.tox

test: test-init
	@tox -e $(TOX_ENV)
