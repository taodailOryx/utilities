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
import random
import sys
import subprocess

from lib.dice import D6_LG


class PetalsAroundTheRose:
    """ Play a game of Petals Around the Rose. """
    def __init__(self, desired_dice: int=4) -> None:
        self.desired_dice: int = desired_dice

        # Setup & validation
        self.dice: dict[int, list[str]] = D6_LG
        self.num_dice = self.set_num_dice()
        self.display_welcome: bool = True

    def set_num_dice(self) -> int:
        """ Validate the number of dice selected. """
        # No fewer than 1 die to play the game
        num_dice: int = max(self.desired_dice, 1)

        # No more than the number of dice in self.dice
        num_dice = min(num_dice, len(self.dice))

        return num_dice

    def get_n_dice(self, n: int) -> list[tuple[int, list[str]]]:
        """ Get n dice from self.dice. """
        if n < 1 or n > len(self.dice):
            return []

        sample_keys: list[int] = random.choices(
            sorted(self.dice),
            k=n
        )

        return [
            (k, self.dice[k])
            for k
            in sample_keys
        ]

    @staticmethod
    def calculate_score(dice_list: list[tuple[int, list[str]]]) -> int:
        """ Calculate the score of a given set of dice. """
        return sum(
            x[0] - 1
            for x
            in dice_list
            if x[0] % 2 > 0
        )

    @staticmethod
    def clear_screen() -> None:
        """ Clear the screen. """
        subprocess.run(['clear'])

    def display(self, dice: list[tuple[int, list[str]]]) -> None:
        """ Display the board for this round. """
        self.clear_screen()

        if self.display_welcome:
            print('Welcome to Petals Around the Rose.\n')
            self.display_welcome = False

        print(
            'The available clues are as follows:\n' \
            '\t1. The name of the game is Petals Around the Rose.\n' \
            '\t2. The answer is a whole number equal to or greater than 0.\n' \
            '\t3. Feel free to try different strategies. ' \
            'The answer will be revealed after each guess.\n\n' \
            'Here are the dice:\n' \
        )

        # Print multi-line or single-line strings for dice
        dice_strings: list[list[str]] = [t[1] for t in dice]

        # Use the first die to determine how many lines to print
        for ix, _ in enumerate(dice_strings[0]):
            print('  '.join(die[ix] for die in dice_strings))

    def play(self) -> None:
        """ Start the game. """

        while True:
            dice: list[tuple[int, list[str]]] = self.get_n_dice(self.num_dice)
            score: int = self.calculate_score(dice)

            self.display(dice)

            validated_guess: int = -1

            while validated_guess < 0:
                guess: str = input('Enter your guess (0 or more): ')

                try:
                    validated_guess = int(guess)
                except (ValueError, TypeError):
                    continue

            if validated_guess == score:
                print('Correct! Congratulations!')
            else:
                print(f'Incorrect, sorry. The answer was {score}.')

            valid_inputs: set[str] = {
                'yes',
                'y',
                'no',
                'n',
            }

            # ANSI sequence to clear the current line
            ansi_clear_line: str = '\x1b[K'
            msg: str = f'{ansi_clear_line}Continue? y/n: '

            while (usr_input := input(msg).strip().lower()) not in valid_inputs:
                # ANSI sequence to move the terminal up one line
                ansi_term_up: str = '\033[1A'

                print(f'{ansi_term_up}\r', end='')
                continue

            if usr_input in ('n', 'no'):
                raise SystemExit(0)

            continue


def get_args(args: list[str]) -> dict[str, str]:
    """ ... """
    supported_args: dict[str, dict[str, list[str]]] = {
        'help': {
            'args': [
                '-h',
                '--help',
            ],
        },
        'dice': {
            'args': [
                '-d',
                '--dice',
            ]
        }
    }

    allowed_switches: list[str] = []

    for arg in supported_args:
        allowed_switches.extend(supported_args[arg]['args'])

    return_args: dict[str, str] = {}
    current_arg: str = ''

    for arg in args:
        if arg.startswith('-'):
            if not current_arg and arg in allowed_switches:
                current_arg = arg
            else:
                return_args[current_arg] = ''
                current_arg = arg
        elif current_arg:
            return_args[current_arg] = arg
            current_arg = ''
        else:
            continue

    # Append the last arg
    if current_arg:
        return_args[current_arg] = ''

    return return_args


if __name__ == '__main__':
    cli_args: list[str] = sys.argv[1:]
    arg_dict: dict[str, str] = get_args(cli_args)

    if '-h' in arg_dict.keys() or '--help' in arg_dict.keys():
        print('Options:\n' \
              '\t-h, --help: This help dialog\n' \
              '\t-d, --dice: Number of dice to play with (1 or more)')
        raise SystemExit(0)

    kwargs: dict = {}

    if '-d' in arg_dict.keys() or '--dice' in arg_dict.keys():
        try:
            dice: str = arg_dict['d']
        except KeyError:
            dice: str = arg_dict['--dice']

        try:
            dice_int = int(dice)
            kwargs['desired_dice'] = dice_int
        except (TypeError, ValueError):
            pass

    potr: PetalsAroundTheRose = PetalsAroundTheRose(**kwargs)

    try:
        potr.play()
    except KeyboardInterrupt:
        # Don't leave the terminal on an input()
        print()

        raise SystemExit(0)
