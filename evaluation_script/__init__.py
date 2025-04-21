import subprocess
import sys
import os
import urllib.request
import json

def is_package_version_on_pypi(package_name, version=None):
    """
    Checks if a package (and optionally a specific version) exists on PyPI.

    Args:
        package_name (str): The name of the package.
        version (str, optional): The specific version to check. Defaults to None.

    Returns:
        bool: True if the package (or specific version) exists, False otherwise.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.load(response)
                latest_version = data["info"]["version"]
                if version is None:
                    print(f"✅ {package_name} exists on PyPI. Latest version is {latest_version}.")
                    return True
                else:
                    all_versions = data["releases"].keys()
                    if version in all_versions:
                        print(f"✅ {package_name}=={version} exists on PyPI. Latest version is {latest_version}.")
                        sys.stdout.flush()
                        return True
                    else:
                        # Use print instead of raising an error to avoid stopping execution
                        print(f"❌ {package_name}=={version} NOT found on PyPI. Latest version is {latest_version}.")
                        sys.stderr.flush()
                        return False
            else:
                print(f"⚠️ Could not fetch data for {package_name} from PyPI (Status: {response.status}).")
                sys.stderr.flush()
                return False
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"❌ Package {package_name} not found on PyPI.")
            sys.stderr.flush()
        else:
            print(f"⚠️ HTTP error occurred while checking {package_name} on PyPI: {e}")
            sys.stderr.flush()
        return False
    except Exception as e:
        print(f"⚠️ An unexpected error occurred while checking {package_name} on PyPI: {e}")
        sys.stderr.flush()
        return False

def install(package):
    # Install a pip python package

    try:
        subprocess.run([sys.executable,"-m","pip","install","--disable-pip-version-check",package])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing {package}: {e.stderr}")
        sys.stderr.flush()
    except FileNotFoundError:
        print("Error: Pip is not found. make sure you have pip installed.")
        sys.stderr.flush()
    except PermissionError:
        print("Error: Permission denied. ")
        sys.stderr.flush()

# Install standard dependencies
install("argcomplete")
install("colorama")
install("pillow")
# install("pykitti")            # Might install additional light deps
# install("rosbags")
# is_package_version_on_pypi("natsort")
install("natsort")
install("lz4")
install("zstandard")

# Install evo from local wheel inside evaluation_script/deps/
this_dir = os.path.dirname(__file__)
evo_wheel_path = os.path.join(this_dir, "deps", "evo-1.31.1-py3-none-any.whl")

# # try:
subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-deps","--disable-pip-version-check", "--ignore-requires-python", evo_wheel_path])

from evo import __version__

def version_to_tuple(version):
    # Split version by '.' and keep only numeric parts
    numeric_parts = []
    for part in version.split("."):
        # Extract leading numeric portion of each part
        numeric_part = "".join(c for c in part if c.isdigit())
        if numeric_part:
            numeric_parts.append(int(numeric_part))
    return tuple(numeric_parts)

evo_version_tuple = version_to_tuple(__version__)
required_version_tuple = (1, 30, 1)

# Check if the version meets the required version
if evo_version_tuple < required_version_tuple:
    raise Exception(
        f"Evo version {__version__} is less than the required version {'.'.join(map(str, required_version_tuple))}. Point_distances not supported."
    )
else:
    print(f"✅ Evo version {__version__} meets the required version.")
    sys.stdout.flush()


from evo.core import sync
from evo.core.trajectory import PoseTrajectory3D
from evo.core.trajectory import Plane
from evo.core.metrics import PoseRelation, Unit

print("✅ evo is installed and available.")
sys.stdout.flush()

from .main import evaluate
