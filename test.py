import importlib.util
import os
import sys
import unittest

from utils import discover_versions


def load_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    versions = discover_versions()

    for version in versions:
        version_dir = os.path.join(os.path.dirname(__file__), "versions", version)
        test_file = os.path.join(version_dir, "test.py")

        if os.path.exists(test_file):
            spec = importlib.util.spec_from_file_location(f"test_{version}", test_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            module_tests = loader.loadTestsFromModule(module)
            suite.addTests(module_tests)

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(load_tests())
