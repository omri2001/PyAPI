SHELL := /bin/sh

.PHONY: dev-setup
dev-setup:
	poetry install



.PHONY: deploy
deploy:
	poetry publish --build

