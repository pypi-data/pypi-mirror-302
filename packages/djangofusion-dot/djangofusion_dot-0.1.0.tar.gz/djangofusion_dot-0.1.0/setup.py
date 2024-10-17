from setuptools import setup, find_packages

setup(
    name='djangofusion-dot',  # Nama package
    version='0.1.0',  # Versi package
    packages=find_packages(),  # Memasukkan semua package yang ditemukan secara otomatis
    install_requires=[
        'Django>=3.0',  # Tambahkan dependensi yang dibutuhkan, jika ada
    ],
    description='A collection of common helpers for Django projects.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/username/djangofusion-dot',  # Sesuaikan dengan URL repository Anda
    author='Alex Sirait',
    author_email='alex.sirait@satnusa.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
