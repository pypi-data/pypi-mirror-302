from setuptools import setup, find_packages

setup(
    name="Iga_Comp_Info",
    version="0.1.0",
    description="Библиотека для вывода системной информации о компьютере",
    author="IGA-PRO (admin-iga)",
    packages=find_packages(),
    install_requires=[
        'psutil'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
