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

import argparse
from pathlib import Path

from .board import Board


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("i", "--input_yaml", type=Path, required=True)

    return parser


def main():
    args = argument_parser().parse_args()
    with args.input_yaml.open() as yaml_file:
        board = Board.from_yaml(yaml_file)
    board.solve()
    print(board)


if __name__ == "__main__":
    main()
