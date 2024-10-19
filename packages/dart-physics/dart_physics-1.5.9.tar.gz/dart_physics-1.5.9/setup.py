from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import gdown
import zipfile

ASSET_URL = "https://drive.google.com/file/d/1U9YeVJfabrSyXPmVQzrxIscDciik3rp4/view?usp=sharing"

class CustomInstallCommand(install):
    def run(self):
        install.run(self)  # Run the default installation process
        self.download_and_extract_assets()  # Then trigger asset downloading and extraction

    def download_and_extract_assets(self):
        ASSET_DIR = os.path.join(os.path.expanduser("~"), ".dart_physics", "assets")
        ZIP_FILE_PATH = os.path.join(ASSET_DIR, "dart_physics_assets.zip")

        if not os.path.exists(ASSET_DIR):
            os.makedirs(ASSET_DIR)
        
        # Check if assets are already downloaded
        if not os.path.exists(ZIP_FILE_PATH):
            print(f"Downloading assets from {ASSET_URL}...")
            gdown.download(ASSET_URL, ZIP_FILE_PATH, quiet=False, fuzzy = True)
            print("Assets downloaded.")
        else:
            print("Assets already exist, skipping download.")

        # Unzip the downloaded file
        if not os.path.exists(os.path.join(ASSET_DIR, 'unzipped_assets_folder')):  # Check if already unzipped
            print("Unzipping assets...")
            with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(ASSET_DIR)
            print("Assets unzipped.")
        else:
            print("Assets already unzipped.")

setup(
    name='dart_physics',
    version='1.5.9',
    packages=find_packages(),
    install_requires=[
        'mujoco',
        'gdown',
        'adam-robotics[jax]==0.3.0',
        'dm_control',
        'loop_rate_limiters',
        'avp_stream',
        'robot_descriptions',
        'obj2mjcf',
        'flask>=3.0.3',
        'psutil', 
        'mediapy', 
        'pyzmq', 
        'grpcio',
        'grpcio-tools',
        'numpy',
        'imageio>=2.36.0',
        'opencv-python',
        'qpsolvers[quadprog] >= 4.3.1',
        'typing_extensions',
        'dexhub-api>=0.3',
        'gdown', 
    ],
    cmdclass={
        'install': CustomInstallCommand,  # Override the install command with custom logic
    },
    author='Younghyo Park',
    author_email='younghyo@mit.edu',
    python_requires='>=3.6',
)
