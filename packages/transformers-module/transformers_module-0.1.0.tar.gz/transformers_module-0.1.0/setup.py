import re

from setuptools import setup

with open("src/__init__.py") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    )[1]

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

extras_require = {}
extras_require["complete"] = sorted(set(sum(extras_require.values(), [])))

setup(
    name="transformers_module",
    package_dir={"": "src"},
    version=version,
    author="",
    author_email="",
    description=long_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    install_requires=open("requirements.txt").readlines(),
    python_requires=">= 3.8, != 3.11.*",
)

