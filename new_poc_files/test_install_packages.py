import subprocess
import sys
import unittest


class TestPackageInstallation(unittest.TestCase):

    def test_pip_install(self):
        result = subprocess.run([sys.executable, 'install_packages.py'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        self.assertIn('Successfully installed requests with pip.', result.stdout)
        self.assertIn('Successfully installed numpy with pip.', result.stdout)

    def test_poetry_install(self):
        result = subprocess.run([sys.executable, 'install_packages.py'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        self.assertIn('Successfully installed packages with poetry.', result.stdout)


if __name__ == '__main__':
    unittest.main()
