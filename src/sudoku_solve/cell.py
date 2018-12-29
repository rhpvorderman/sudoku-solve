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


class Cell(object):
    def __init__(self):
        # Possible values are 1-9
        self.possible_values = set(range(1, 9 + 1))
        self.fixed_value = None

    def set_value(self, value: int):
        if value not in set(range(1, 9 + 1)):
            raise ValueError("Value must be in range 1-9")
        self.possible_values = set([value])
        self.fixed_value = value

    def update_with_fixed(self, fixed_set: Set[int]):
        """"""
        if self.fixed_value is None:
            self.possible_values -= fixed_set
            self.fix_if_certain()

    def update_with_possible(self, possible_list: List[Set[int]]):
        if self.fixed_value is None:
            possible_values_in_other_cells = set()
            for values in possible_list:
                possible_values_in_other_cells.update(values)
            must_be_one_of = (self.possible_values -
                              possible_values_in_other_cells)
            if len(must_be_one_of) > 0:
                self.possible_values = must_be_one_of
                self.fix_if_certain()

    def fix_if_certain(self):
        if self.fixed_value is None and len(self.possible_values) == 1:
            # Pop from a copy so self.possible_values will keep it's one
            # element
            self.fixed_value = self.possible_values.copy().pop()

    def __str__(self):
        return " " if self.fixed_value is None else str(self.fixed_value)
