import doctest
import coverage

cov = coverage.Coverage(source=['main','nn_handler'])
cov.start()
doctest.testfile('README.md')
cov.stop()
cov.html_report(directory='covhtml')