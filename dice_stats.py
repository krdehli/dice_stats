import argparse
import sys
import argparse
import math
import re

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
    def variance(self) -> float:
        return self.__variance


    @property
    def standard_deviation(self) -> float:
        return self.__standard_deviation


    @property
    def coefficient_of_variance(self) -> float:
        return self.__coefficient_of_variance


    def __calculate_mean(self):
        self.__mean = self.__offset + self.__num_dice * (self.__faces + 1) / 2


    def __calculate_variance(self):
        self.__variance = self.__num_dice * (self.__faces**2 - 1) / 12


    def __calculate_standard_deviation(self):
        self.__standard_deviation = math.sqrt(self.__variance)


    def __calculate_coefficient_of_variance(self):
        self.__coefficient_of_variance = self.__standard_deviation / self.__mean;


    def __calculate_stats(self):
        self.__calculate_mean()
        self.__calculate_variance()
        self.__calculate_standard_deviation()
        self.__calculate_coefficient_of_variance()


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

    for roll in args.rolls:
        print(f'Roll: {roll} | mean: {roll.mean} | coefficient of variance: {100 * roll.coefficient_of_variance:.2f}%')

    sys.exit()


if __name__ == '__main__':
    main()