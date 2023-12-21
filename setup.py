import sys
from os import path

from setuptools import find_packages, setup

import versioneer

# NOTE: This file must remain Python 2 compatible for the foreseeable future,
# to ensure that we error out properly for people with outdated setuptools
# and/or pip.
min_version = (3, 6)
if sys.version_info < min_version:
    error = """
nsls2-detector-handlers does not support Python {0}.{1}.
Python {2}.{3} and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
""".format(
        *(sys.version_info[:2] + min_version)
    )
    sys.exit(error)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open(path.join(here, "requirements.txt")) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [line for line in requirements_file.read().splitlines() if not line.startswith("#")]


setup(
    name="nsls2-detector-handlers",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Staging repo for handlers specific to NSLS-II",
    long_description=readme,
    author="Brookhaven National Laboratory",
    author_email="dama@bnl.gov",
    url="https://github.com/bluesky/nsls2-detector-handlers",
    python_requires=">={}".format(".".join(str(n) for n in min_version)),
    packages=find_packages(exclude=["docs", "tests"]),
    entry_points={
        "databroker.handlers": [
            "ZEBRA_HDF51 = nsls2_detector_handlers.srx_flyscans:ZebraHDF5Handler",
            "SIS_HDF51 = nsls2_detector_handlers.srx_flyscans:ZebraHDF5Handler",
            "PIZZABOX_AN_FILE_TXT = nsls2_detector_handlers.pizzabox:PizzaBoxAnHandlerTxt",
            "PIZZABOX_DI_FILE_TXT = nsls2_detector_handlers.pizzabox:PizzaBoxDIHandlerTxt",
            "PIZZABOX_ENC_FILE_TXT = nsls2_detector_handlers.pizzabox:PizzaBoxEncHandlerTxt",
            "PIZZABOX_AN_FILE_TXT_PD = nsls2_detector_handlers.pizzabox:PizzaBoxAnHandlerTxtPD",
            "PIZZABOX_DI_FILE_TXT_PD = nsls2_detector_handlers.pizzabox:PizzaBoxDIHandlerTxtPD",
            "PIZZABOX_ENC_FILE_TXT_PD = nsls2_detector_handlers.pizzabox:PizzaBoxEncHandlerTxtPD",
            "ELECTROMETER = nsls2_detector_handlers.electrometer:ElectrometerBinFileHandler",
            "AD_TIFF_GERM = nsls2_detector_handlers.germ:AreaDetectorTiffHandlerGERM",
            "AD_HDF5_GERM = nsls2_detector_handlers.germ:AreaDetectorHDF5HandlerGERM",
            "VIDEO_STREAM_HDF5 = nsls2_detector_handlers.webcam:VideoStreamHDF5Handler",
        ],
    },
    include_package_data=True,
    package_data={
        "nsls2_detector_handlers": [
            # When adding files here, remember to update MANIFEST.in as well,
            # or else they will not be included in the distribution on PyPI!
            # 'path/to/data_file',
        ]
    },
    install_requires=requirements,
    license="BSD (3-clause)",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
)
