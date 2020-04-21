.PHONY: all

all:
	pylint -E pymakehelper
	pyflakes pymakehelper
	pytest
