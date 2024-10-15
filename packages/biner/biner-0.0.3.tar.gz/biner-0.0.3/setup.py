from setuptools import setup, find_packages

with open("readme.md", "r") as f:
    description = f.read()

setup(
    name='biner',  # Nama package kamu di PyPI
    version='0.0.3',  # Versi package
    packages=find_packages(),  # Cari semua modul secara otomatis
    description='package biner',
    long_description=description,
    long_description_content_type='text/markdown',
    author='Kelompok 7B',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
) 