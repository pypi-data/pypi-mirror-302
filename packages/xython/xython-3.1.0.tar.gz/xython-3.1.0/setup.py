# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

#from sphinx.setup_command import BuildDoc
#commands["build_sphinx"] = BuildDoc
# install_requires=['pyperclip', 'pywinauto', 'chardet','pygetwindow','pyautogui','unittest','paho-mqtt','pandas','pywin32','PySide6','korean_lunar_calendar','screeninfo','zipfile','','' ],


with open("README.md", "rt", encoding='UTF8') as fh:
    long_description = fh.read()
setup(
    name='xython',
    version='3.1.0',
    url='https://www.xython.co.kr',
    install_requires=['' ],
    download_url='https://github.com/sjpark/xython/archive/v3.1.0.tar.gz',
    author='sjpkorea',
    author_email='sjpkorea@naver.com',
    description="EXCEL, WORD, OUTLOOK, REGEX, COLORING, HWP BY PYTHON",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "xython": ["*.*"],
        },
    long_description_content_type="text/markdown",
    long_description=open('README.md', "r", encoding='UTF8').read(),
    python_requires='>=3.8',
    zip_safe=False,
    classifiers=['License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
    project_urls = {
      'Documentation': 'https://sjpkorea.github.io/xython.github.io/',
      'Link 1': 'https://www.xython.co.kr',
    }
    )

