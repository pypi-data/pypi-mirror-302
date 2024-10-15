from setuptools import setup, find_packages

setup(
    name='SimplePy2Exe',
    version='0.1.1',
    author='Hilton Queiroz Rebello',
    author_email='rebello.hiltonqueiroz@gmail.com',
    description='Transforme seu projeto Python em um executável',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hqr90/py2exe',
    packages=find_packages(include=["launch*"]),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,  # Inclui arquivos especificados no MANIFEST.in
    python_requires='>=3.8',
    install_requires=[
        "altgraph",
        "packaging",
        "pefile",
        "pillow",
        "pyinstaller",
        "pyinstaller-hooks-contrib",
        "PyQt5",
        "pywin32-ctypes",
    ]
)