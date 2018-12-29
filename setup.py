# Copyright (C) 2018 Ruben Vorderman
# This file is part of sudoku-solve
#
# sudoku-solve is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# sudoku-solve is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with sudoku-solve.  If not, see <https://www.gnu.org/licenses/

from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name="sudoku-solve",
    version="0.1.0-dev",
    description="A program to solve sudoku puzzles",
    author="Ruben Vorderman",
    author_email="RubenVorderman@xs4all.nl",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="AGPL-3.0-or-later",
    keywords="sudoku solve",
    zip_safe=False,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={},
    url="https://github.com/rhpvorderman/sudoku-solve",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    install_requires=[
        "pyyaml"
    ],
    entry_points={
        'console_scripts': ['sudoku-solve=sudoku_solve.main:main']
    }
)
