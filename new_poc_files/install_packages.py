import subprocess
import sys


def install_with_pip(package):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f'Successfully installed {package} with pip.')
    except subprocess.CalledProcessError as e:
        print(f'Failed to install {package} with pip. Error: {e}')


def install_with_poetry():
    try:
        subprocess.check_call(['poetry', 'install'])
        print('Successfully installed packages with poetry.')
    except subprocess.CalledProcessError as e:
        print(f'Failed to install packages with poetry. Error: {e}')


def main():
    packages = ['requests', 'numpy']  # Example packages
    for package in packages:
        install_with_pip(package)
    install_with_poetry()


if __name__ == '__main__':
    main()
