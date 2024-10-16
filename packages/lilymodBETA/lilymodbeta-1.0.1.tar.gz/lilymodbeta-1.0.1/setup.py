from setuptools import setup, find_packages

setup(
    name='lilymodBETA',
    version='1.0.1',
    description='So simple, its criminal',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Izaiyah Stokes',
    author_email='zeroth.bat@gmail.com',
    url='https://github.com/d34d0s/Anntwinetta',
    packages=find_packages(),
    package_data={"lilymodBETA": ['lilymod/assets/*', 'lilymod/bin/*']},
    install_requires=[
        "GLFW",
        "PyGLM",
        "PyOpenGL",
        "ModernGL",
        "Pygame-CE",
        "Numpy",
        "Numba",
        "SetupTools",
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)