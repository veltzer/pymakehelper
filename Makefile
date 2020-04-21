.PHONY: all

all:
	@pylint -E pymakehelper
	@pyflakes pymakehelper
	@pytest 2>&1 >/dev/null
