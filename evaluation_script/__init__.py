
import subprocess
import sys

def install(package):

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")


install("numpy==1.24.4")
install("scipy==1.10.1")
install("matplotlib==3.7.5")
install("pyyaml==6.0.2")
install("tqdm")
install("argcomplete==3.6.2")
install("colorama==0.4.6")
install("pillow==10.4.0")
install("pykitti")            # Might install additional light deps
install("rosbags==0.9.23")
install("natsort==8.4.0")
install("lz4==4.3.3")
install("zstandard==0.23.0")
# install("evo==1.31.1")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-deps", "deps/evo-1.31.1-py3-none-any.whl"])
except subprocess.CalledProcessError as e:
    print(f"Failed to install evo: {e}")

# try:
#
import evo as iamtired
subprocess.check_call(['echo', '✅ evo is installed and available.'])
# except ImportError as e:
#     print("❌ evo is NOT available:", e)

from .main import evaluate
