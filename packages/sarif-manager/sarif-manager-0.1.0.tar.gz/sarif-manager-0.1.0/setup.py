"""Setup script"""
import setuptools
import os
import re

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")
TESTS_REQUIRE = ["coverage", "pytest"]


def get_version():
    init = open(os.path.join(HERE, "sarif_manager", "version.py")).read()
    return VERSION_RE.search(init).group(1)


def get_description():
    return open(
        os.path.join(os.path.abspath(HERE), "README.md"), encoding="utf-8"
    ).read()


setuptools.setup(
    name="sarif-manager",
    include_package_data=True,
    version=get_version(),
    author="Kinnaird McQuade",
    author_email="kinnaird@nightvision.net",
    description="Parse SARIF files for different providers.",
    packages=setuptools.find_packages(exclude=["test*"]),
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/nvsecurity/api-validator",
    tests_require=TESTS_REQUIRE,
    install_requires=[
        "beautifulsoup4",
        "click",
        "click-option-group",
        "loguru",
        "markdown",
        "requests",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": "sarif-manager=sarif_manager.bin.cli:main"},
    zip_safe=True,
    keywords="sarif",
    python_requires=">=3.11",
)
