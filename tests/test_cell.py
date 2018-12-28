# Copyright (C) 2018 Ruben Vorderman
# This file is part of sudoku-solve
#
# pytest-workflow is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# pytest-workflow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pytest-workflow.  If not, see <https://www.gnu.org/licenses/

from sudoku_solve.board import Cell


def test_init():
    cell = Cell()
    assert cell.possible_values == set(range(1, 10))
    assert cell.fixed_value is None


def test_update_with_fixed():
    cell = Cell()
    cell.update_with_fixed({1, 2, 3})
    assert cell.possible_values == {4, 5, 6, 7, 8, 9}
