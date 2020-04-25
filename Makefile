.PHONY: all

all:
	@pylint --rcfile=.pylint.rc --reports=n --score=n pymakehelper tests
	@pyflakes pymakehelper tests
	@pytest -qq > /dev/null
