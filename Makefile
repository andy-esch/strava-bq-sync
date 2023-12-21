.PHONY: test

test:
	poetry run pytest tests/

local:
	poetry run functions-framework --target stravabqsync_listener --debug
