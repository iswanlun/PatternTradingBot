import unittest, os, sys
sys.path.append(os.getcwd() + "\\src")

from slq_lite_database import Storage
from position import Position



class DBTesting(unittest.TestCase):

    def setUp(self) -> None:
        self.storage = Storage()

    def test_open_positions(self):

        position1 = Position.create_position(100, 'eth')
        position2 = Position.create_position(120, 'btc')
        position3 = Position.create_position(321, 'ltc')

        self.storage.new_position(position1)
        self.storage.new_position(position2)
        self.storage.new_position(position3)

        open_positions = []

        open_positions = self.storage.open_positions()

        self.assertEqual(len(open_positions), 3)

    def test_close_positions(test):
        pass


unittest.main()