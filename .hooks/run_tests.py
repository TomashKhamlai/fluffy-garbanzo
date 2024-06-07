import subprocess


def main():
    try:
        result = subprocess.run(['pytest'], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f'Tests failed with exit code {e.returncode}')
        return e.returncode


if __name__ == '__main__':
    exit(main())
