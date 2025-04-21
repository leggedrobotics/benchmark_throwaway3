import subprocess
import sys
import os
# import urllib.request
# import json

# def is_package_version_on_pypi(package_name, version):
#     url = f"https://pypi.org/pypi/{package_name}/json"
#     try:
#         with urllib.request.urlopen(url) as response:
#             if response.status == 200:
#                 data = json.load(response)
#                 all_versions = data["releases"].keys()
#                 if version in all_versions:
#                     print(f"✅ {package_name}=={version} exists on PyPI.")
#                     return True
#                 else:
#                     print(f"❌ {package_name}=={version} NOT found on PyPI.")
#                     return False
#     except Exception as e:
#         print(f"⚠️ Could not check {package_name} version on PyPI: {e}")
#         return False


# package = "evo"
# version = "1.31.1"

# if is_package_version_on_pypi(package, version):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}=={version}"])

def install(package):
    # Install a pip python package

    # Args:
    #     package ([str]): Package name with version
    try:
        subprocess.run([sys.executable,"-m","pip","install",package])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing {package}: {e.stderr}")
    except FileNotFoundError:
        print("Error: Pip is not found. make sure you have pip installed.")
    except PermissionError:
        print("Error: Permission denied. ")



# def install(package):
#     # try:
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])
#     # except subprocess.CalledProcessError as e:
#     #     print(f"❌ Failed to install {package}: {e}")

# Install standard dependencies
install("numpy")
install("evo")
install("scipy==1.10.1")
# install("matplotlib==3.7.5")
# install("pyyaml==6.0.2")
install("tqdm")
# install("argcomplete==3.6.2")
# install("colorama==0.4.6")
# install("pillow==10.4.0")
# install("pykitti")            # Might install additional light deps
# install("rosbags==0.9.23")
install("natsort==8.4.0")
# install("lz4==4.3.3")
# install("zstandard==0.23.0")

# Install evo from local wheel inside evaluation_script/deps/
this_dir = os.path.dirname(__file__)
evo_wheel_path = os.path.join(this_dir, "deps", "evo-1.31.1-py3-none-any.whl")

# try:
subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-deps", evo_wheel_path])
import evo as afterfunc
from evo.core import sync
from evo.core.trajectory import PoseTrajectory3D
from evo.core.trajectory import Plane
from evo.core.metrics import PoseRelation, Unit
from evo.tools import file_interface
import evo.main_ape as main_ape
import evo.main_rpe as main_rpe
# print("✅ evo is installed and available.")
# except subprocess.CalledProcessError as e:
#     print(f"❌ Failed to install evo wheel: {e}")
# except ImportError as e:
#     print(f"❌ Failed to import evo after install: {e}")

#
from .main import evaluate
