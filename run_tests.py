import unittest

# run from "LISP/tests" directory
loader = unittest.TestLoader()
suite = loader.discover(start_dir="LISP/tests", pattern="test_*.py")

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
