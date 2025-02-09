import sys
from packaging.version import Version

REQUIRED_VERSION = (3, 8)  # Example: Python 3.8

# Get current Python version
current_version = sys.version_info

# Compare versions
if current_version >= REQUIRED_VERSION:
    print("Python version is sufficient.")
else:
    print("Python version is too old.")

def get_packages(pkgs):
    versions = []
    for p in pkgs:
        try:
            imported = __import__(p)
            try:
                versions.append(imported.__version__)
            except AttributeError:
                try:
                    versions.append(imported.version)
                except AttributeError:
                    try:
                        versions.append(imported.version_info)
                    except AttributeError:
                        versions.append('0.0')
        except ImportError:
            print(f'[FAIL]: {p} is not installed and/or cannot be imported.')
            versions.append('N/A')
    return versions


def check_packages(d):

    versions = get_packages(d.keys())

    for (pkg_name, suggested_ver), actual_ver in zip(d.items(), versions):
        if actual_ver == 'N/A':
            continue
        actual_ver, suggested_ver = Version(actual_ver), Version(suggested_ver)
        if pkg_name == "matplotlib" and actual_ver == Version("3.8"):
            print(f'[FAIL] {pkg_name} {actual_ver}, please upgrade to {suggested_ver} >= matplotlib > 3.8')
        elif actual_ver < suggested_ver:
            print(f'[FAIL] {pkg_name} {actual_ver}, please upgrade to >= {suggested_ver}')
        else:
            print(f'[OK] {pkg_name} {actual_ver}')



if __name__ == '__main__':
    d = {
        'numpy': '2.2.2',
        'scipy': '1.15.1',
        'matplotlib': '3.10.0',
        'scikit-learn': '1.6.1',
        'pandas': '2.2.3'
    }
    check_packages(d)