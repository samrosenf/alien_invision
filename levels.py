import os.path
from csv import reader


class LevelFileError(Exception):
    """Level file doesn't exist."""
    pass


def load_level_file(filepath):
    """Load a level file to a list.
        The level file is in csv format.
        Each row represnet a row of aliens in the game.
        Each number indicates the level of the alien (from 1 - 9)
        There are maximum 7 rows of aliens.
    """
    # Make sure file exist
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as read_obj:
                csv_reader = reader(read_obj)
                data_level = list(csv_reader)
                data_level = [[int(j) for j in row] for row in data_level]
        except:
            print("level file couldn't be parsed")
            data_level = [1 for _ in range(9)]
    else:
        raise LevelFileError("the level file coudn't be found")
    return data_level


def main():
    data_level = load_level_file('levels/demo_level.csv')


if __name__ == "__main__":
    main()
