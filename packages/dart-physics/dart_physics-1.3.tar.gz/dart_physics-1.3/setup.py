from setuptools import setup, find_packages

setup(
    name='dart_physics',
    version='1.3',
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
        'importlib-metadata',  # Added to satisfy Dash requirement
        'nest-asyncio',        # Added to satisfy Dash and orbax-checkpoint requirements
        'plotly>=5.0.0',       # Added to satisfy Dash requirement
        'pandas>=1.0',         # Added to satisfy objaverse and open3d requirements
        'scikit-learn>=0.21',  # Added to satisfy open3d requirement
        'msgpack',             # Added to satisfy orbax-checkpoint requirement
        'sympy',               # Added to satisfy PyTorch requirement
        'PyOpenGL==3.1.0',     # Locked to avoid conflict with pyrender
    ],
    author='Younghyo Park',
    author_email='younghyo@mit.edu',
    python_requires='>=3.6',
)
