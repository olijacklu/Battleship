from engine import *
import pytest


'''
File used to test basic functionalities of the game
'''

#Test if boat coordinates map to a real boat

grid = Grid(10)

assert grid.size == 10

boat = Boat(0, 4, 0, 0, grid.grid, False)

assert boat.get_invalid() is False

#Check if coordinates are correct
boat = Boat(0, 4, 1, 0, grid.grid, False)

assert boat.get_invalid() is True

boat = Boat(0, 4, 1, 0, grid.grid, False, 4)

assert boat.get_invalid() is True

boat = Boat(0, 4, 1, 0, grid.grid, False, 4)

assert boat.get_invalid() is True

#Check if sized is correct
boat = Boat(0, 4, 1, 1, grid.grid, False, 5)

assert boat.get_invalid() is False


def test_boats():
    with pytest.raises(RuntimeError):
        boat = Boat(0, 4, 1, 1, grid.grid, False, 6)

