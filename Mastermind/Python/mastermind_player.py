#!/usr/bin/env python3
#
import random
import logging

class MastermindPlayer:
    """
        The rules of the Mastermind game, as done on the server
    """
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.NUMBER_OF_COLORS = 6
        self.LIST_SIZE = 4
        self.colors = self._pick_colors()
        logging.debug(f'Server picked: {self.colors}')

    def _pick_colors(self):
        colors = list()
        for i in range(self.LIST_SIZE):
            colors.append(random.randint(0, self.NUMBER_OF_COLORS-1))
        return colors

    def grade(self, client_string):
        "Compute the grade to send back to the client"
        client_colors = client_string.split()
        if len(client_colors) != self.LIST_SIZE:
            logging.debug(f'Wrong number of colors from client: {client_colors}')
            return (False, '0 0\r\n')
        correct_colors = 0
        correct_location = 0
        for i in range(self.LIST_SIZE):
            int_color = int(client_colors[i])
            if int(int_color) in self.colors:
                correct_colors += 1
            if int_color == self.colors[i]:
                correct_location += 1;
        done = (correct_colors == 4) and (correct_location == 4)
        return (done, f'{correct_colors} {correct_location}\r\n')