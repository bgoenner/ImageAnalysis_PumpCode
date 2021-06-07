import sys
import os

sys.path.append(os.getcwd() + '\\src')

from unittest.mock import patch
import unittest
import importlib.util
import containers
#import main from ./../src

import imageCapture

class terminalInputTest(unittest.TestCase):


    @patch('builtins.input', return_value="-i")
    def test_displayInfo(self, input):
        testString = "Capture Device: " + "None" + "\n" + \
            "Input File: " + "None" + "\n" + \
            "Output File: " + "None" + "\n" + \
            "Mode: " + "1" + "\n" + \
            "Mask: " + "None" + "\n" + \
            "Area: " + "None" + "\n" +\
            "Buffer: " + "None" + "\n"

        #stacks = containers.get_input_stacks()


        self.assertEqual(testString, imageCapture.readInput(input))

    def test_displayHelp(self):
        pass
    def test_setCatpure0(self):
        pass
    def test_startVideo(self):
        pass


if __name__ == "__main__":
    unittest.main()