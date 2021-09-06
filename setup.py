from setuptools import find_packages, setup


def get_install_requirements(filename):
    """
    Get non-dev packages required for installation.

    :param filename: Name of requirements file.
    :return: List of none-dev packages.
    """

    return open("requirements/" + filename).read().splitlines()


setup(
    name='cpimgtxt',
    packages=find_packages(include=['cp_img_txt']),
    version='0.1.0',
    description='Copy text from a copied image.',
    author='Daviti Magaldadze',
    author_email='davitako777@gmail.com',
    license='GPLv2',
    python_requires=">=3.6",
    url="https://github.com/davidako/copy-img-text",
    install_requires=get_install_requirements("default.txt"),
    setup_requires=['pytest-runner'],
    tests_require=get_install_requirements("dev.txt"),
    scripts=['cpimgtxt'],
)
