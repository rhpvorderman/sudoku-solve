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

import textwrap
from pathlib import Path

from sudoku_solve.board import Board


def test_init():
    board = Board()
    assert len(board.matrix) == 9
    assert len(board.matrix[3]) == 9
    assert board[3, 4].fixed_value is None


def test_from_yaml():
    board = Board.from_yaml(textwrap.dedent(
        """\
        0:
          2: 5
          7: 6
        4:
          2: 7
        """)
    )
    assert board[0, 2].fixed_value == 5
    assert board[0, 7].fixed_value == 6
    assert board[4, 2].fixed_value == 7
    assert board[0, 0].fixed_value is None


def test_solve():
    easy_sudoku = Path(__file__).parent / Path("sudokus") / Path("easy.yml")
    with easy_sudoku.open() as easy:
        board = Board.from_yaml(easy)
    board.solve()
    assert board.possible_numbers_left() == 0
