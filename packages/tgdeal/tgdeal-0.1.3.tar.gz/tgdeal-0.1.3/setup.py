from setuptools import find_packages, setup
import subprocess
import pkg_resources
import sys

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


def check_and_install(package, spec_name=None):
    try:
        pkg_resources.require(package)
        print(f"{package} is already installed.")

    except pkg_resources.DistributionNotFound:
        subprocess.check_call([sys.executable, "-m", "pip", "install", spec_name or package])


setup(
    name='tgdeal',
    packages=find_packages(exclude=['tests']),
    version='0.1.3',
    description='Python-пакет, предоставляющий полноценный API-клиент для работы с B2B API сервиса. Предназначен для использования как конечными пользователями, так и партнерскими сервисами.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='TeleDealer',
    license='MIT',
    install_requires=[
        'simple_singleton',
        'pydantic',
        'httpx'
    ]
)
