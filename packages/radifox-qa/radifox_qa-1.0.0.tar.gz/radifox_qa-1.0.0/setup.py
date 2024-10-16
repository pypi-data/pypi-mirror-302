from pathlib import Path
from setuptools import setup, find_namespace_packages


__package_name__ = "radifox-qa"


def get_version_and_cmdclass(pkg_path):
    """Load version.py module without importing the whole package.

    Template code from miniver
    """
    import os
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("version", os.path.join(pkg_path, "_version.py"))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.get_cmdclass(pkg_path)


__version__, cmdclass = get_version_and_cmdclass('radifox/qa')

setup(
    name=__package_name__,
    version=__version__,
    cmdclass=cmdclass,
    author="JH-MIPC",
    author_email="jhmipc@jh.edu",
    url="https://github.com/jh-mipc/radifox-qa",
    description="A quality assurance webapp for the RADIFOX framework.",
    long_description=(Path(__file__).parent.resolve() / "README.md").read_text(),
    long_description_content_type="text/markdown",
    license="Apache License, 2.0",
    packages=find_namespace_packages(include=['radifox.*']),
    entry_points={
        "console_scripts": [
            "radifox-qa=radifox.qa.run:run",
        ]
    },
    install_requires=[
        "flask",
        "gunicorn",
        "pyyaml",
        "radifox>=2.1.0",
    ],
    package_data={
        "radifox.qa": [
            "templates/*.html",
        ]
    },
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
