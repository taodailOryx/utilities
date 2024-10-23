""" Copyright (C) 2023 Drew Simonson

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import copy
import random

from pathlib import Path


class MatchedMap:
    """ If a directory named `.bs/` exists in this directory, and a file named `names`
    exists in that directory, a list of names will be pulled from that file automatically
    when this file is executed.
    """
    def __init__(self, names_list: list[str], mandatory_matches: dict[str, str]) -> None:
        self.names_list: list[str] = names_list
        self.names: list[str] = []

        self.mandatory_matches: dict[str, str] = mandatory_matches

        self.match_to_self: bool = False
        self.match_to_reciprocal: bool = False
        self.randomize_name_order: bool = False

        self.__forbidden_matches: dict[str, str] = {}
        self.__last_map: dict[str, str] = {}
        self.__validate_setup()

    def __validate_setup(self) -> None:
        """ Validate input and perform any setup.
        :returnval None:
        """
        if not self.names_list:
            raise ValueError('Provide a list of strings of names')

        duplicate_names: set[str] = set(
            [
                n
                for n
                in self.names_list
                if self.names_list.count(n) > 1
            ]
        )

        if duplicate_names:
            msg: str = f'Duplicate entry in names_list ({duplicate_names.pop()})' \

            raise ValueError(msg)

        try:
            self.names = [str(n) for n in self.names_list]
        except ValueError:
            raise

    def __shuffle_names(self) -> None:
        """ Shuffle self.names in place.
        :returnval None:
        """
        random.shuffle(self.names)

    def __recursive_mm_gen(self, names: list[str],
                            current_mm: dict[str, str]) -> dict[str, str]:

        """ Recursively generate a new matched map, following the constraints
        established.
        :returnval dict[str, str]: The matched map, or an empty dict if no map
                is possible
        """
        if not names:
            return current_mm

        for name in names:
            if name not in current_mm.keys():
                current_mm[name] = ''

        for key_name in current_mm.keys():
            if current_mm[key_name]:
                continue
            for list_name in names:
                if list_name == key_name and not self.match_to_self:
                    continue
                if current_mm[list_name] == key_name and not self.match_to_reciprocal:
                    continue
                if (key_name in self.__forbidden_matches
                        and self.__forbidden_matches[key_name] == list_name):
                    continue

                new_mm: dict[str, str] = copy.deepcopy(current_mm)
                new_names: list[str] = copy.deepcopy(names)
                new_mm[key_name] = list_name
                new_names.remove(list_name)
                new_map: dict[str, str] = self.__recursive_mm_gen(new_names, new_mm)

                if new_map:
                    return new_map
                else:
                    continue
        return current_mm or {}

    def set_forbidden_matches(self, forbidden_dict: dict[str, str]) -> None:
        """ Pass a dictionary with any forbidden matches.
        :param forbidden_dict dict[str, str]: A dictionary of forbidden matches
        :returnval None:
        """
        for k, v in forbidden_dict.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValueError(
                    'Invalid name (should be str): ' \
                    f'"{k if not isinstance(k, str) else v}"'
                )

            if k not in self.names or v not in self.names:
                raise ValueError(
                    f'Unrecognized name: "{k if k not in self.names else v}"'
                )

        self.__forbidden_matches = forbidden_dict

    def generate_matched_map(self) -> dict[str, str]:
        """ Use the list of names provided to generate a matched map.
        :returnval dict[str, str]: The generated map
        """
        if not self.names:
            return {}

        if self.match_to_reciprocal and len(self.names) % 2 != 0:
            raise ValueError('Number of names must be even for reciprocal matching')

        if self.randomize_name_order:
            # Randomize the order so the generation is not deterministic (i.e., the first correct
            # solution found should be different each time [subject to the whims of the PRNG])
            self.__shuffle_names()

        matched_map: dict[str, str] = self.__recursive_mm_gen(self.names, self.mandatory_matches)

        if not matched_map:
            raise ValueError('Cannot generate map')

        # We have to randomize again, otherwise the mandatory matches always come out first
        values: list[tuple] = [_ for _ in matched_map.items()]
        random.shuffle(values)
        matched_map = dict(values)

        self.__last_map = matched_map

        return self.__last_map

    def get_last_map(self) -> dict[str, str]:
        """ Retrieve the last successful map generated.
        :returnval dict[str, str]: The last map successfully generated
        """
        return self.__last_map


if __name__ == '__main__':
    names_file_path: Path = Path('./.bs/names')
    names_list: list[str] = []

    if names_file_path.exists():
        with open(names_file_path, encoding='utf8') as f:
            names_list = [n.strip() for n in f.readlines()]
    else:
        sentinel_value: str = '$$END$$'

        print(f'When done entering names, enter {sentinel_value}.')
        print('Enter names now, each followed by ENTER key:')

        while True:
            name: str = input().strip()

            if name == sentinel_value:
                print(f'\n{"-" * 80}\n')
                break

            if name:
                names_list.append(name)

    if len(names_list) < 2:
        raise ValueError('Enter at least 2 names')

    mandatory_matches: dict[str, str] = {}

    mm: MatchedMap = MatchedMap(names_list=names_list, mandatory_matches=mandatory_matches)
    mm.randomize_name_order = True
    matches: dict[str, str] = mm.generate_matched_map()

    for k, v in matches.items():
        print(f'{k} → {v}')
