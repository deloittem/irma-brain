TESTS=./tests
RESULTS=${TESTS}/results
PACKAGES=brain
OPTIONS=--cover-erase --with-coverage --cover-package=${PACKAGES} --cover-html --cover-html-dir=${RESULTS} --with-xunit --xunit-file=${RESULTS}/brain_xunit.xml


test-env:
	mkdir -p ${RESULTS}
	export IRMA_BRAIN_CFG_PATH=${TESTS} && PYTHONPATH=. python tests/__init__.py
	# the args given to create_user.py must match vars defined in the tests/brain.ini conf file
	export IRMA_BRAIN_CFG_PATH=${TESTS} && PYTHONPATH=. python scripts/create_user.py  test_brain test_brain test_brain


test: test-env
	nosetests ${TESTS}


testc: test-env
	pylint ${PACKAGES} 2>&1 > ${RESULTS}/brain.pylint || exit 0
	nosetests ${OPTIONS} ${TESTS}
