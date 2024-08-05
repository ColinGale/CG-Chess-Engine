from bs4 import BeautifulSoup
import urllib.request
import random

from constants import *

class Book:
    def __init__(self):
        self.move_dict = {}
        self.move_number = 0
        self.move_index = []

        self.get_move_table(BASE_URL + OPENING)


    def get_move_table(self, url):
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, LXML)

        # finds DIV with id=sidebar2
        sidebar = soup.find(DIV, {ID: SIDEBAR_2})
        table_list = sidebar.find_all(TABLE)

        # looks at first table under sidebar2
        position_table = table_list[0]
        row_list = position_table.find_all(TR)

        # every other TR because of HTML code
        for index in range(1, len(row_list), 2):
            current_row = row_list[index]
            href = current_row.a[HREF]
            move = current_row.a.text
            move = move.split(".")[-1][1:]
            self.move_dict[move] = href
            self.move_index.append(move)


    def opening_moves(self, notation, url):
        if notation in self.move_dict:
            url = self.move_dict[notation]
            self.clear()
            self.get_move_table(BASE_URL + url)
            self.move_number += 1
            #print(self.move_number)

        num = random.randint(0, len(self.move_dict) // 4)
        move_string = self.move_index[num]

        return move_string, url

    def clear(self):
        self.move_dict = {}
        self.move_index = []


    def __str__(self):
        return str(self.move_dict)

