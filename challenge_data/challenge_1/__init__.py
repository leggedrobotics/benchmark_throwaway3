
import subprocess
import sys

def install(package):

    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("numpy")
install("tqdm")
install("evo==1.31.1")
install("matplotlib")
install("scipy")

from .main import evaluate
