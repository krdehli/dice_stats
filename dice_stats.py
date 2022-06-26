import argparse
import sys
import argparse
import math
import re
from collections.abc import Collection, Mapping
from typing import Any

class DiceRoll:
    def __init__(self, faces: int, num_dice: int = 1, offset: int | float = 0):
        if not isinstance(faces, int):
            raise TypeError('faces must be an int')

        if not isinstance(num_dice, int):
            raise TypeError('num_dice be an int')

        if not isinstance(offset, (int, float)):
            raise TypeError('offset must be a float or int')

        if faces < 1:
            raise ValueError('faces must be greater than 0')

        if num_dice < 1:
            raise ValueError('num_dice must be greater than 0')
        
        self.__faces = faces
        self.__num_dice = num_dice
        self.__offset = offset
        
        self.__calculate_stats()


    def __str__(self) -> str:
        if self.__offset != 0 or isinstance(self.__offset, float):
            return f'{self.__num_dice}d{self.__faces}+{self.__offset}'
        else:
            return f'{self.__num_dice}d{self.__faces}'


    def __repr__(self) -> str:
        return f'DiceRoll({self.__faces}, {self.__num_dice}, {self.__offset})'


    def __format__(self, spec: str) -> str:
        return self.__str__().__format__(spec)


    __parse_pattern = re.compile('(\d+)(?:d|D)(\d+)(?: *\+ *(\d+))?')

    @classmethod
    def from_string(cls, string: str):
        match = cls.__parse_pattern.match(string)
        if match is None:
            raise ValueError('Invalid dice notation')
        
        if match.group(3) is None:
            return cls(int(match.group(2)), int(match.group(1)))
        else:
            return cls(int(match.group(2)), int(match.group(1)), int(match.group(3)))


    @property
    def faces(self) -> int:
        return self.__faces;


    @faces.setter
    def faces(self, value: int):
        self.__faces = value
        self.__calculate_stats()


    @property 
    def num_dice(self) -> int:
        return self.__num_dice;


    @num_dice.setter
    def num_dice(self, value: int):
        self.__num_dice = value;
        self.__calculate_stats()


    @property
    def offset(self) -> float:
        return self.__offset


    @offset.setter
    def offset(self, value: float):
        self.__offset = value
        self.__calculate_stats()


    @property
    def mean(self) -> float:
        return self.__mean


    @property
    def var(self) -> float:
        return self.__var


    @property
    def sd(self) -> float:
        return self.__sd


    @property
    def cv(self) -> float:
        return self.__cv


    def __calculate_mean(self):
        self.__mean = self.__offset + self.__num_dice * (self.__faces + 1) / 2


    def __calculate_variance(self):
        self.__var = self.__num_dice * (self.__faces**2 - 1) / 12


    def __calculate_standard_deviation(self):
        self.__sd = math.sqrt(self.__var)


    def __calculate_coefficient_of_variance(self):
        self.__cv = self.__sd / self.__mean;


    def __calculate_stats(self):
        self.__calculate_mean()
        self.__calculate_variance()
        self.__calculate_standard_deviation()
        self.__calculate_coefficient_of_variance()


def column_widths(data: Collection[Mapping[str, Any]]) -> dict[str, int]:
    widths: dict[str, int] = {}
    for elem in data:
        for key in elem:
            if key not in widths:
                widths[key] = len(key)
            widths[key] = max(widths[key], len(str(elem[key])))
    return widths


def format_as_table(data: Collection[Mapping[str, Any]]) -> str:
    widths = column_widths(data)

    header = ' '.join(f'{key:{width}}' for key, width in widths.items())
    header_sep = ' '.join('-' * width for _, width in widths.items())
    rows = [' '.join(f'{value:{width}}' for value, width in [(row[key] or '', widths[key]) for key in widths]) for row in data]

    return '\n'.join([header, header_sep, *rows])
    

def format_as_list(data: Collection[Mapping[str, Any]]) -> str:
    widths = column_widths(data)

    lines = [' | '.join(f'{key}: {value:{width}}' for key, value, width in [(key, line[key] or '', widths[key]) for key in widths]) for line in data]
    return '\n'.join(lines)


LONG_FIELD_NAMES: dict[str, str] = {
    'roll': 'Roll',
    'mean': 'Mean',
    'cv': 'Coefficient of Variance'
}

SHORT_FIELD_NAMES: dict[str, str] = {
    'roll': 'Roll',
    'mean': 'µ',
    'cv': 'Cv'
}

def main():
    parser = argparse.ArgumentParser(
        description='Provide simple statistical values for given dice rolls'
    )
    parser.add_argument(
        'rolls', 
        type=DiceRoll.from_string,
        nargs='+', 
        metavar='ROLL',
        help='A dice roll given with the notation NdS+C where N is the number of dice '
             'in the roll (min. 1), S is the number of sides on the die (min. 1), '
             'and C is a constant modifier to the roll. The "+C" component is optional'
    )
    parser.add_argument(
        '-a', '--abbreviate',
        action='store_true',
        help='use abbreviated names for stat fields '
             '(e.g. µ for mean and Cv for coefficient of variance)'
    )
    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['list', 'table'],
        default='list',
        help='the output format of the stats (defaults to list)'
    )

    args = parser.parse_args()

    names = SHORT_FIELD_NAMES if args.abbreviate else LONG_FIELD_NAMES
    data = [{names['roll']: roll, names['mean']: roll.mean, names['cv']: f'{100 * roll.cv:.2f}%'} for roll in args.rolls]

    match args.format:
        case 'list': 
            print(format_as_list(data))
        case 'table': 
            print(format_as_table(data))

    sys.exit()


if __name__ == '__main__':
    main()