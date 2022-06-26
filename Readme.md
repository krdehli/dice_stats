# Dice Stats

A simple command line utility to display the statistical properties of dice roll

## Examples
Show the stats of a d20
```sh
$ ./dice_stats.py 1d20
```

Show the stas of a modified roll, using abbreviated property names
```sh
$ ./dice_stats.py --abbreviate 1d10+1
```

Compare the stats of several dice in a table
```sh
$ ./dice_stats.py --format table 1d4 1d6 1d8 1d10 1d12 1d20 1d100
```

## Requirements
You need a Python 3 interpreter to run the program.