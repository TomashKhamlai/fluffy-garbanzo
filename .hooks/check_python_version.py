import sys


def read_python_version_file():
    with open('.python-version') as f:
        return f.read().strip()


def get_current_python_version():
    return f'{sys.version_info.major}.{sys.version_info.minor}'


def main():
    required_version = read_python_version_file()
    current_version = get_current_python_version()

    if float(current_version) < float(required_version):
        print(f'Error: You are using Python {current_version}, but this project requires Python {required_version}.')
        print('Please upgrade your Python version.')
        sys.exit(1)
    else:
        print(f'Python version {current_version} is correct.')


if __name__ == '__main__':
    main()
