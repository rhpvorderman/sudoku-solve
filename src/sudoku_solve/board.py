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

from typing import Dict, List, Set, Tuple

import yaml

def squares_sets() -> List[Set[Tuple[int, int]]]:
    sets = dict()
    for x in range(9):
        for y in range(9):
            index_x = x // 3
            index_y = y // 3
            dict_index = str(index_x) + str(index_y)
            if x % 3 == 0 and y % 3 == 0:
                sets[dict_index] = set()
            sets[dict_index].add((x, y))
    return sets.values()


SQUARES_SETS = squares_sets()


def in_square_set(coordinate: Tuple[int, int]) -> Set[Tuple[int, int]]:
    for square_set in SQUARES_SETS:
        if coordinate in square_set:
            return square_set
        raise ValueError("{0} not found in {1}".format(
            coordinate, SQUARES_SETS
        ))


class Cell(object):
    def __init__(self):
        # Possible values are 1-9
        self.possible_values = set(range(1, 9 + 1))
        self.fixed_value = None

    def set_value(self, value: int):
        if value not in set(range(1, 9 + 1)):
            raise ValueError("Value must be in range 1-9")
        self.possible_values = set(value)
        self.fixed_value = value

    def update_with_fixed(self, fixed_set: Set[int]):
        """"""
        if self.fixed_value is not None:
            self.possible_values -= fixed_set
            self.fix_if_certain()

    def update_with_possible(self, possible_set: Set[Set[int]]):
        if self.fixed_value is not None:
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

    def __str__(self):
        return " " if self.fixed_value is None else str(self.fixed_value)


class Board(object):
    def __init__(self):
        self.matrix = [[Cell()] * 9 for i in range(9)]
        self.sets_dict = self._create_sets_dict()

    def __getitem__(self, key: Tuple[int, int]):
        x, y = key
        return self.matrix[x][y]

    def __str__(self):
        lines = []
        line_separator = 9 * "----" + "-\n"
        lines.append(line_separator)
        for row in self.matrix:
            line_string = ""
            for cell in row:
                line_string += "| {0} ".format(cell)
            lines.append(line_string + "|\n")
            lines.append(line_separator)
        return "".join(lines)

    @classmethod
    def from_dict(cls,dictionary: Dict[int, Dict[int, int]]):
        board = cls.__init__()
        for x, y_dictionary in dictionary.items():
            for y, value in y_dictionary.items():
                board[x,y].set_value(value)
        return board

    @classmethod
    def from_yaml(cls, yaml_string: str):
        return cls.from_dict(yaml.safe_load(yaml_string))

    def get_row(self, index: int):
        return self.matrix[index]

    def get_column(self, index: int):
        return [row[index] for row in self.matrix]

    def _create_sets_dict(self) -> Dict[
        Tuple[int, int], List[Set[Tuple[int, int]]]]:
        sets_dict = dict()
        for x, row in enumerate(self.matrix):
            for y, cell in (enumerate(row)):
                coordinate = (x, y)
                row_set = set([(x, i) for i, _ in enumerate(row)])
                column_set = set(
                    [(i, y) for i, column in enumerate(self.get_column(x))])
                square_set = in_square_set(coordinate)
                row_set.discard(coordinate)
                column_set.discard(coordinate)
                square_set.discard(coordinate)
                sets_dict[coordinate] = [
                    row_set,
                    column_set,
                    square_set
                ]
        return sets_dict

    def coordinates_to_fixed_set(
            self, coordinates: Set[Tuple[int, int]]) -> Set[int]:
        fixed_set = set(
            [self[coordinate].fixed_value for coordinate in coordinates])
        fixed_set.discard(None)
        return fixed_set

    def coordinates_to_possible_set(
            self, coordinates: Set[Tuple[int, int]]) -> Set[Set[int]]:
        possible_set = set(
            [self[coordinate].possible_values for coordinate in coordinates])
        return possible_set

    def update_cel_fixed(self, coordinate: Tuple[int, int]):
        coordinate_sets = self.sets_dict[coordinate]
        for coordinate_set in coordinate_sets:
            fixed_numbers = self.coordinates_to_fixed_set(coordinate_set)
            self[coordinate].update_with_fixed(fixed_numbers)

    def update_cel_possible_values(self, coordinate: Tuple[int, int]):
        coordinate_sets = self.sets_dict[coordinate]
        for coordinate_set in coordinate_sets:
            possible_numbers = self.coordinates_to_possible_set(coordinate_set)
            self[coordinate].update_with_possible(possible_numbers)

    def solve_iteration(self):
        for x, row in enumerate(self.matrix):
            for y, cell in enumerate(row):
                if cell.fixed_value is not None:
                    self.update_cel_fixed((x, y))
                if cell.fixed_value is not None:
                    self.update_cel_possible_values((x, y))

    def possible_numbers_left(self) -> int:
        possible_numbers_left = 0
        for row in self.matrix:
            for cell in row:
                if cell.fixed_value is None:
                    possible_numbers_left += len(cell.possible_values)
        return possible_numbers_left

    def solve(self, max_iterations=1000):
        possible_numbers_left = self.possible_numbers_left()
        for iteration in max_iterations:
            self.solve_iteration()
            if self.possible_numbers_left() == 0:
                return iteration
            elif self.possible_numbers_left() == possible_numbers_left:
                raise ValueError("Puzzle unsolvable from this point")
            possible_numbers_left = self.possible_numbers_left()
        raise ValueError(
            "Puzzle not solvable in {0} iterations".format(max_iterations))
