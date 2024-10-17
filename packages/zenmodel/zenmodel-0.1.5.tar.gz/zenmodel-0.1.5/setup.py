from setuptools import setup, find_packages

setup(
    name="zenmodel",
    version="0.1.5",
    packages=find_packages(include=['zenmodel', 'zenmodel.*', 'pyprocessor', 'pyprocessor.*']),
    package_data={'zenmodel': ['__init__.py'], 'pyprocessor': ['*.py']},
    install_requires=[
    ],
    author="Clay Zhang",
    author_email="ambler2clay@gmail.com",
    description="zenmodel python processor",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zenmodel/zenmodel",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
