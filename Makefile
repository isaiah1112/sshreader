.PHONY: docker docker-push test test-clean test-init

DOCKER_TAG = isaiah1112/sshreader:latest
TOX_ENV = $(shell grep -o 'py[0-9][0-9]' $(PWD)/tox.ini | tail -1)

docker:
	@docker build -t $(DOCKER_TAG) .

docker-push:
	@docker push $(DOCKER_TAG)

test-init:
	@pip install -r virtualenv tox

test-clean:
	@rm $(PWD)/.tox

test: test-init
	@tox -e $(TOX_ENV)
