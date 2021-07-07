import sys
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

from . import common

class PokerSort:
    def __init__(self):
        self.card_num = 3
        self.assign_list = None
        self.random_seed = None
        self.fold_mode = False
        self.canvas_width = common.poker_canvas_width
        self.canvas_height = common.poker_canbas_height
        self.card_name = ['back',
                          'heart1',
                          'heart2',
                          'heart3',
                          'heart4',
                          'heart5',
                          'heart6',
                          'heart7',
                          'heart8',
                          'heart9',
                          'heart10',
                          'heart11',
                          'heart12',
                          'heart13',
                        ]
        self.card_img_list = []

    def 發牌(self):
        if common.current_algorithm:
            print(common.current_algorithm, " 已在執行中\n一次只限執行1種演算法")
            sys.exit()
        
        common.current_algorithm =  "排序撲克"

        self.lazy_init()

    def lazy_init(self):
        #load card images
        self.load_card_images()

        # tk canvas
        self.root = tk.Tk()
        self.root.geometry("{}x{}+0+0".format(self.canvas_width,self.canvas_height))
        self.canvas = tk.Canvas(self.root, bg = '#c7fcda',
               width=self.canvas_width, height=self.canvas_height,
               )
        self.canvas.pack()

        self.canvas.update()

    def load_card_images(self):
        pass

        #_im = Image.open(Path(__file__).parent / 'images' / (name + '.png'))       
        #common_images[name] = ImageTk.PhotoImage(_im)

排序撲克 = PokerSort()