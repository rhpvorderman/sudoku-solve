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

from typing import Set, Tuple


class Cell(object):
    def __init__(self):
        # Possible values are 1-9
        self.possible_values = set(range(1, 9 + 1))
        self.fixed_value = None

    def update_with_fixed(self, fixed_set: Set[int]):
        """"""
        self.possible_values -= fixed_set
        self.fix_if_certain()

    def update_with_possible(self, possible_set: Set[Set[int]]):
        possible_values_in_other_cells = {}
        for values in possible_set:
            possible_values_in_other_cells.update(values)
        must_be_one_of = self.possible_values - possible_values_in_other_cells
        if len(must_be_one_of) > 0:
            self.possible_values = must_be_one_of
            self.fix_if_certain()

    def fix_if_certain(self):
        if self.fixed_value is not None and len(self.possible_values) == 1:
            # Pop from a copy so self.possible_values will keep it's one
            # element
            self.fixed_value = self.possible_values.copy().pop()


class Board(object):
    def __init__(self):
        self.matrix = [[Cell()] * 9 for i in range(9)]

    def __getitem__(self, key: Tuple[int, int]):
        x, y = key
        return self.matrix[x][y]
