from setuptools import find_packages, setup

setup(
    name="touchid",
    packages=find_packages(),
    include_package_data=True,
    version="2.0.0",
    description="Access the Touch ID sensor",
    long_description="`touchid` provides an easy to use API for accessing the Touch ID sensor via Apple's LocalAuthentication framework",
    keywords=["touch-id", "LocalAuthentication", "LAContext"],
    license="MIT",
    author="Lukas Kollmer",
    author_email="lukas.kollmer@gmail.com",
    maintainer="Ethan Henderson",
    maintainer_email="ethan.henderson.1998@gmail.com",
    url="https://github.com/parafoxia/python-touch-id/",
    install_requires=["pyobjc-framework-LocalAuthentication"],
)
