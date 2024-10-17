from setuptools import setup, find_packages

setup(
    name='asm-chill_py',
    version='0.1.0',
    author='atharva bodade',
    author_email='atharvabodade@gmail.com',
    description='A Python library for simulating assembly language programming',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/atharvapatil1210/asm_py',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
)

