import sys
import tkinter as tk
import tkinter.font as font
import random
from PIL import Image, ImageTk
from pathlib import Path
import time

from . import common

class 搜尋猜數錯誤(Exception):
    pass

class SearchGuess:
    ALGORITHM_NAME = "搜尋猜數"
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 800

    BACKGROUND_NAME = 'search_guess_bg'
    LOGO_NAME = 'search_guess_logo'

    DEFAULT_LOWER_BOUND = 0
    DEFAULT_UPPER_BOUND = 99

    LOGO_X = 50
    LOGO_Y = 0

    
    def __init__(self):
        self.puzzle_answer = None  # bin str
        self.puzzle_lower_bound = None
        self.puzzle_upper_bound = None
        

    def 產生題目(self, *args, **kwargs):
        if common.current_algorithm is not None and common.current_algorithm != self.ALGORITHM_NAME :
            raise 搜尋猜數錯誤('\n\n'+common.current_algorithm + "演算法已在執行中\n無法同時執行"+self.ALGORITHM_NAME)
        common.current_algorithm =  self.ALGORITHM_NAME

        if len(args) == 0:
            self.puzzle_lower_bound = self.DEFAULT_LOWER_BOUND
            self.puzzle_upper_bound = self.DEFAULT_UPPER_BOUND
            if '隨機種子' in kwargs:
                #print('seed: ', kwargs['隨機種子'])
                random.seed(kwargs['隨機種子'])
            tmp = random.randint(self.puzzle_lower_bound,
                            self.puzzle_upper_bound)
            self.puzzle_answer = bin(tmp)
            #print('answer: ', self.puzzle_answer)


        self._do_init()

        self.canvas.update()

    def _do_init(self):
        self.gui_init()
        self.set_background()
        self.set_logo()
        self.set_assets()

    def gui_init(self):
        self.root = tk.Tk()
        self.normal_font = font.Font(size=13, weight=font.NORMAL, family='Consolas')
        self.result_font = font.Font(size=55, weight=font.NORMAL, family='Consolas')
        self.root.geometry("{}x{}+0+0".format(self.CANVAS_WIDTH,  self.CANVAS_HEIGHT))
        self.canvas = tk.Canvas(self.root,
                    width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack()

        # load background


    def set_assets(self):
        pass


    def set_background(self):
        path = Path(__file__).parent / 'images' / (self.BACKGROUND_NAME + '.png')
                
        _im = Image.open(path)
        self.bg_img = ImageTk.PhotoImage(_im)
        self.bg_id = self.canvas.create_image(
                0,
                0,
                image=self.bg_img,
                anchor=tk.NW,
                )

    def set_logo(self):
        path = Path(__file__).parent / 'images' / (self.LOGO_NAME + '.png')
        
        
        _im = Image.open(path)
        self.logo_img = ImageTk.PhotoImage(_im)
        self.logo_id = self.canvas.create_image(
                self.LOGO_X,
                self.LOGO_Y,
                image=self.logo_img,
                anchor=tk.NW,
                )

搜尋猜數 = SearchGuess()  