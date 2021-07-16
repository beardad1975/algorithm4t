import sys
import tkinter as tk
import tkinter.font as font
import random
from PIL import Image, ImageTk
from pathlib import Path
import time
from itertools import cycle

from . import common

class 搜尋猜數錯誤(Exception):
    pass

class SearchGuess:
    ALGORITHM_NAME = "搜尋猜數"
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 800

    BACKGROUND_NAME = 'search_guess_bg'
    LOGO_NAME = 'search_guess_logo'
    RULER_NAME = 'ruler'

    DEFAULT_LOWER_BOUND = 100
    DEFAULT_UPPER_BOUND = 150

    LOGO_X = 50
    LOGO_Y = 0

    RULER_X = 150
    RULER_Y = 160

    PUZZLE_X = 200
    PUZZLE_Y = 90

    COLOR_LIST = ['#349beb','#eb02eb','#11db02','#fc8c03',]
    COLOR_POOL = cycle(COLOR_LIST)

    BAR_X = 160
    BAR_WIDTH = 30
    BAR_X_RIGHT = BAR_X + BAR_WIDTH
    BAR_MIN_Y = 205
    BAR_MAX_Y = 680
    BAR_MAX_HEIGHT = BAR_MAX_Y - BAR_MIN_Y
    THIN_BAR_WIDTH = 5
    THIN_BAR_GAP = 3
    THIN_BAR_X = BAR_X_RIGHT + THIN_BAR_GAP
    THIN_BAR_X_RIGHT = THIN_BAR_X + THIN_BAR_WIDTH

    LINE_X = 20
    BOUND_TEXT_X = 35
    
    LOWER_BOUND_TEXT_SHIFTY = 8
    UPPER_BOUND_TEXT_SHIFTY = -50
    
    def __init__(self):
        self.puzzle_answer = None  # bin str
        self.puzzle_lower_bound = None
        self.puzzle_upper_bound = None
        self.answer_lower_bound = None
        self.answer_upper_bound = None
        self.bound_delta = None
        self.bar_id = None
        self.thin_bar_id = None
        self.current_color = next(self.COLOR_POOL)

    def 產生題目(self, *args, **kwargs):
        if common.current_algorithm is not None and common.current_algorithm != self.ALGORITHM_NAME :
            raise 搜尋猜數錯誤('\n\n'+common.current_algorithm + "演算法已在執行中\n無法同時執行"+self.ALGORITHM_NAME)
        common.current_algorithm =  self.ALGORITHM_NAME

        if len(args) == 0:
            self.puzzle_lower_bound = self.DEFAULT_LOWER_BOUND
            self.answer_lower_bound = self.DEFAULT_LOWER_BOUND
            self.puzzle_upper_bound = self.DEFAULT_UPPER_BOUND
            self.answer_upper_bound = self.DEFAULT_UPPER_BOUND
            self.bound_delta = self.answer_upper_bound - self.answer_lower_bound
            if '隨機種子' in kwargs:
                #print('seed: ', kwargs['隨機種子'])
                random.seed(kwargs['隨機種子'])
            tmp = random.randint(self.puzzle_lower_bound,
                            self.puzzle_upper_bound)
            self.puzzle_answer = bin(tmp)
            #print('answer: ', self.puzzle_answer)


        self._do_init()

        self.canvas.update()

    def delay(self):
        #pass
        time.sleep(0.0001)  

    def _do_init(self):
        self.gui_init()
        self.set_background()
        self.set_logo()
        self.set_assets()
        self.bar_init()
        #self.adjsut_lower_bound(new_y)

        
    def bar_init(self):
        # create lower bound line dot and text
        self.lower_bound_lineid = self.canvas.create_line(
                self.LINE_X, self.BAR_MAX_Y, 
                self.THIN_BAR_X_RIGHT, self.BAR_MAX_Y,
                fill=self.current_color,
                
                width=2,
                dash=(7,))
        self.lower_bound_dotid = self.canvas.create_oval(
                self.LINE_X - 6 , self.BAR_MAX_Y - 6, 
                self.LINE_X + 5, self.BAR_MAX_Y + 5,
                fill=self.current_color,
                width=0)
        self.lower_bound_textid = self.canvas.create_text(
                self.BOUND_TEXT_X , 
                self.BAR_MAX_Y + self.LOWER_BOUND_TEXT_SHIFTY,
                anchor=tk.NW,
                justify=tk.CENTER,
                font = self.normal_font,
                text='{}\n答案下限'.format(self.puzzle_lower_bound))
        
        # create upper bound line dot and text
        self.upper_bound_lineid = self.canvas.create_line(
                self.LINE_X, self.BAR_MAX_Y, 
                self.THIN_BAR_X_RIGHT, self.BAR_MAX_Y,
                fill=self.current_color,
                
                width=2,
                dash=(7,)
                )
        self.upper_bound_dotid = self.canvas.create_oval(
                self.LINE_X - 6 , self.BAR_MAX_Y - 6, 
                self.LINE_X + 5, self.BAR_MAX_Y + 5,
                fill=self.current_color,
                width=0, )
        self.upper_bound_textid = self.canvas.create_text(
                self.BOUND_TEXT_X , 
                self.BAR_MAX_Y + self.UPPER_BOUND_TEXT_SHIFTY,
                anchor=tk.NW,
                justify=tk.CENTER,
                font = self.normal_font,
                text='答案上限\n{}'.format(self.puzzle_upper_bound))


        # animate bar from lower bound to upper bound 
        if self.bound_delta < 100:
            num_step = 1

        for n in range(self.answer_lower_bound, 
                       self.answer_upper_bound + 1,
                       num_step):
            self.redraw_bar(self.answer_lower_bound, n)

        

    def redraw_bar(self, lower_num, upper_num):
        if lower_num > upper_num :
            raise 搜尋猜數錯誤('redraw_bar: lowernum > upper_num')

        if type(lower_num) is not int or type(upper_num) is not int:
            raise 搜尋猜數錯誤('redraw_bar: lowernum or upper_num not int')

        

        if self.bar_id is not None:
            self.canvas.delete(self.bar_id)
            self.bar_id = None

        if self.thin_bar_id is not None:
            self.canvas.delete(self.thin_bar_id)
            self.thin_bar_id = None

        big_y = self.num2y(lower_num)
        small_y = self.num2y(upper_num)

        

        # redarw bar and thin bar 
        self.bar_id = self.canvas.create_rectangle(
                        self.BAR_X, 
                        small_y,
                        self.BAR_X_RIGHT, 
                        big_y,
                        width=0,    
                        fill=self.current_color,)

        self.thin_bar_id = self.canvas.create_rectangle(
                        self.THIN_BAR_X, 
                        small_y,
                        self.THIN_BAR_X_RIGHT, 
                        big_y,
                        width=0,    
                        fill=self.current_color,)
        
        # update upper bound line, dot and text
        self.canvas.coords(self.upper_bound_lineid, 
                           self.LINE_X, 
                           small_y,
                           self.THIN_BAR_X_RIGHT, 
                           small_y, )
        self.canvas.itemconfigure(self.upper_bound_lineid,
                        fill=self.current_color,)

        self.canvas.coords(self.upper_bound_dotid,
                self.LINE_X - 6 , small_y - 6, 
                self.LINE_X + 5, small_y + 5 )
        self.canvas.itemconfigure(self.upper_bound_dotid,
                        fill=self.current_color,)
        
        self.canvas.coords(self.upper_bound_textid,
                self.BOUND_TEXT_X , 
                small_y + self.UPPER_BOUND_TEXT_SHIFTY,)
        self.canvas.itemconfigure(self.upper_bound_textid,
                text='答案上限\n{}'.format(upper_num) )

        # update lower bound line, dot and text
        self.canvas.coords(self.lower_bound_lineid, 
                           self.LINE_X, 
                           big_y,
                           self.THIN_BAR_X_RIGHT, 
                           big_y, )
        self.canvas.itemconfigure(self.lower_bound_lineid,
                        fill=self.current_color,)

        self.canvas.coords(self.lower_bound_dotid,
                self.LINE_X - 6 , big_y - 6, 
                self.LINE_X + 5, big_y + 5 )
        self.canvas.itemconfigure(self.lower_bound_dotid,
                        fill=self.current_color,)
        
        self.canvas.coords(self.lower_bound_textid,
                self.BOUND_TEXT_X , 
                big_y + self.LOWER_BOUND_TEXT_SHIFTY,)
        self.canvas.itemconfigure(self.lower_bound_textid,
                text='{}\n答案下限'.format(lower_num) )

        self.canvas.update()
        self.delay()

    def adjust_upper_bound(self, value):
        if value > self.puzzle_upper_bound:
            raise 搜尋猜數錯誤


    def num2y(self, n):
        # to do :value check
        tmp =  self.BAR_MAX_Y - (n-self.answer_lower_bound)* self.BAR_MAX_HEIGHT / self.bound_delta 
        return int(tmp)

    def gui_init(self):
        self.root = tk.Tk()
        self.normal_font = font.Font(size=14, weight=font.NORMAL, family='Consolas')
        self.result_font = font.Font(size=55, weight=font.NORMAL, family='Consolas')
        self.root.geometry("{}x{}+0+0".format(self.CANVAS_WIDTH,  self.CANVAS_HEIGHT))
        self.canvas = tk.Canvas(self.root,
                    width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack()

        # load background


    def set_assets(self):
        # put ruler
        path = Path(__file__).parent / 'images' / (self.RULER_NAME + '.png')     
        _im = Image.open(path)
        self.ruler_img = ImageTk.PhotoImage(_im)
        self.ruler_id = self.canvas.create_image(
                self.RULER_X,
                self.RULER_Y,
                image=self.ruler_img,
                anchor=tk.NW )

        # put puzzle
        puzzle_text = '請猜出範圍{}~{}內的整數答案'.format(
                    self.puzzle_lower_bound,
                    self.puzzle_upper_bound
                    )
        self.puzzle_id = self.canvas.create_text(
                self.PUZZLE_X,
                self.PUZZLE_Y,
                font=self.normal_font,
                text=puzzle_text,
                anchor=tk.CENTER,
                justify=tk.CENTER )
        
        # load arrow and hide

         
        # self.bar_id = self.canvas.create_rectangle(
        #                 self.BAR_X, 
        #                 self.BAR_MIN_Y,
        #                 self.BAR_X + self.BAR_WIDTH, 
        #                 self.BAR_MAX_Y,
        #                 width=0,    
        #                 fill='#349beb',
        #             ) 

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

