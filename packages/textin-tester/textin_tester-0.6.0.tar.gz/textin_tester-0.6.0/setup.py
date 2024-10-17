# setup.py
from setuptools import setup, find_packages

setup(
    name="textin_tester",
    version="0.6.0",
    packages=find_packages(include=['textin_tester','textin_tester.tester', 'textin_tester.tester.*', 'textin_tester.doc']),
    package_data={
        'textin_tester.doc': ['*.png', '*.jpg', '*.jpeg', '*.gif'],
        'textin_tester': ['*.py']
    },
    entry_points={
        "console_scripts": [
            "run_test=textin_tester.run_test:main",
        ],
    },
    long_description=open("textin_tester/README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

# python setup.py sdist bdist_wheel
