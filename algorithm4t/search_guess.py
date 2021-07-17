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
    ARROW_NAME = 'search_arrow'

    DEFAULT_LOWER_BOUND = 0
    DEFAULT_UPPER_BOUND = 100

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
    CHANGE_SCALE_TEXT_X = 30
    BOUND_TEXT_X = 35

    RULER_TEXT_X = 225
    
    ARROW_X = 220

    LOWER_BOUND_TEXT_SHIFTY = 8
    UPPER_BOUND_TEXT_SHIFTY = -50

    MIN_SCALE_DELTA = 10
    ZOOM_IN_RATE = 0.03
    
    def __init__(self):
        self.puzzle_lower_bound = None
        self.puzzle_upper_bound = None
        self.puzzle_answer = None  # bin str
        
        self.ruler_lower_bound = None
        self.ruler_upper_bound = None
        self.ruler_bound_delta = None
        
        self.lower_bound = None 
        self.upper_bound = None
        
        self.bar_id = None
        self.thin_bar_id = None
        self.current_color = next(self.COLOR_POOL)

        self.arrow_num = None
        self.arrow_visible =None

    def 產生題目(self, *args, **kwargs):
        if common.current_algorithm is not None and common.current_algorithm != self.ALGORITHM_NAME :
            raise 搜尋猜數錯誤('\n\n'+common.current_algorithm + "演算法已在執行中\n無法同時執行"+self.ALGORITHM_NAME)
        common.current_algorithm =  self.ALGORITHM_NAME

        if len(args) == 0:
            self.puzzle_lower_bound = self.DEFAULT_LOWER_BOUND
            self.puzzle_upper_bound = self.DEFAULT_UPPER_BOUND

            self.ruler_lower_bound = self.puzzle_lower_bound
            self.ruler_upper_bound = self.puzzle_upper_bound
            self.ruler_bound_delta = self.ruler_upper_bound - self.ruler_lower_bound

            self.lower_bound = self.puzzle_lower_bound
            self.upper_bound = self.puzzle_upper_bound
            
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
        self.ruler_init()
        
        #test
        self.change_lower_bound(20)
        self.change_upper_bound(21)
        
        #self.change_scale(11,80)
        
    def ruler_init(self):
        # create lower bound line dot and text
        self.lower_bound_lineid = self.canvas.create_line(
                self.LINE_X, self.BAR_MAX_Y, 
                self.THIN_BAR_X_RIGHT, self.BAR_MAX_Y,
                fill=self.current_color,
                state=tk.NORMAL,
                width=2,
                dash=(7,))
        self.lower_bound_dotid = self.canvas.create_oval(
                self.LINE_X - 6 , self.BAR_MAX_Y - 6, 
                self.LINE_X + 5, self.BAR_MAX_Y + 5,
                fill=self.current_color,
                state=tk.NORMAL,
                width=0)
        self.lower_bound_textid = self.canvas.create_text(
                self.BOUND_TEXT_X , 
                self.BAR_MAX_Y + self.LOWER_BOUND_TEXT_SHIFTY,
                anchor=tk.NW,
                justify=tk.CENTER,
                state=tk.NORMAL,
                font = self.normal_font,
                text='{}\n下限'.format(self.ruler_lower_bound))
        
        # create upper bound line dot and text
        self.upper_bound_lineid = self.canvas.create_line(
                self.LINE_X, self.BAR_MAX_Y, 
                self.THIN_BAR_X_RIGHT, self.BAR_MAX_Y,
                fill=self.current_color,
                state=tk.NORMAL,
                width=2,
                dash=(7,)
                )
        self.upper_bound_dotid = self.canvas.create_oval(
                self.LINE_X - 6 , self.BAR_MAX_Y - 6, 
                self.LINE_X + 5, self.BAR_MAX_Y + 5,
                fill=self.current_color,
                state=tk.NORMAL,
                width=0, )
        self.upper_bound_textid = self.canvas.create_text(
                self.BOUND_TEXT_X , 
                self.BAR_MAX_Y + self.UPPER_BOUND_TEXT_SHIFTY,
                anchor=tk.NW,
                justify=tk.CENTER,
                state=tk.NORMAL,
                font = self.normal_font,
                text='上限\n{}'.format(self.ruler_upper_bound))

        # ruler text
        self.ruler_upper_textid = self.canvas.create_text(
                self.RULER_TEXT_X , 
                self.BAR_MIN_Y,
                anchor=tk.W,
                justify=tk.LEFT,
                state=tk.NORMAL,
                font = self.small_font,
                text='{}'.format(self.ruler_upper_bound))

        self.ruler_lower_textid = self.canvas.create_text(
                self.RULER_TEXT_X , 
                self.BAR_MAX_Y,
                anchor=tk.W,
                justify=tk.LEFT,
                state=tk.NORMAL,
                font = self.small_font,
                text='{}'.format(self.ruler_lower_bound))

        self.scale_changing_textid = self.canvas.create_text(
                self.CHANGE_SCALE_TEXT_X, 
                (self.BAR_MAX_Y + self.BAR_MIN_Y)//2,
                anchor=tk.W,
                justify=tk.LEFT,
                state=tk.HIDDEN,
                font = self.normal_font,
                text='[縮放尺度範圍]')

        # raise arrow above ruler text
        self.canvas.tag_raise(self.ruler_upper_textid, self.ruler_lower_textid)
        self.canvas.tag_raise(self.arrow_id, self.ruler_upper_textid)

        # animate bar from lower bound to upper bound 

        if self.ruler_bound_delta <= 100:
            num_step = 1
        else:
            num_step = 2

        for n in range(self.ruler_lower_bound, 
                       self.ruler_upper_bound + 1,
                       num_step):
            self.draw_ruler(self.ruler_lower_bound, n)

        

    def draw_ruler(self, lower_num, upper_num, show_gizmo=True):
        if lower_num > upper_num :
            raise 搜尋猜數錯誤('redraw_bar: lowernum > upper_num')

        if type(lower_num) is not int or type(upper_num) is not int:
            raise 搜尋猜數錯誤('redraw_bar: lowernum or upper_num not int')

        
        # delete old bar if necessary
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
        

        
        

        # handle both bound text display
        if show_gizmo :
            # update upper bound line, dot 
            self.canvas.coords(self.upper_bound_lineid, 
                            self.LINE_X, 
                            small_y,
                            self.THIN_BAR_X_RIGHT, 
                            small_y, )
            self.canvas.itemconfigure(self.upper_bound_lineid,
                            state=tk.NORMAL,
                            fill=self.current_color,)

            self.canvas.coords(self.upper_bound_dotid,
                    self.LINE_X - 6 , small_y - 6, 
                    self.LINE_X + 5, small_y + 5 )
            self.canvas.itemconfigure(self.upper_bound_dotid,
                            state=tk.NORMAL,
                            fill=self.current_color,)
            
            # update lower bound line, dot 
            self.canvas.coords(self.lower_bound_lineid, 
                            self.LINE_X, 
                            big_y,
                            self.THIN_BAR_X_RIGHT, 
                            big_y, )
            self.canvas.itemconfigure(self.lower_bound_lineid,
                            state=tk.NORMAL,
                            fill=self.current_color,)

            self.canvas.coords(self.lower_bound_dotid,
                    self.LINE_X - 6 , big_y - 6, 
                    self.LINE_X + 5, big_y + 5 )
            self.canvas.itemconfigure(self.lower_bound_dotid,
                            state=tk.NORMAL,
                            fill=self.current_color,)

            self.canvas.coords(self.upper_bound_textid,
                    self.BOUND_TEXT_X , 
                    small_y + self.UPPER_BOUND_TEXT_SHIFTY,)
            self.canvas.itemconfigure(self.upper_bound_textid,
                    state=tk.NORMAL,
                    text='上限\n{}'.format(upper_num) )

            self.canvas.coords(self.lower_bound_textid,
                    self.BOUND_TEXT_X , 
                    big_y + self.LOWER_BOUND_TEXT_SHIFTY,)
            self.canvas.itemconfigure(self.lower_bound_textid,
                    state=tk.NORMAL,
                    text='{}\n下限'.format(lower_num) )
        else:
            # hide line,  dot ,text
            self.canvas.itemconfigure(self.upper_bound_lineid,
                                      state=tk.HIDDEN)
            self.canvas.itemconfigure(self.upper_bound_dotid,
                                      state=tk.HIDDEN)
            self.canvas.itemconfigure(self.lower_bound_lineid,
                                      state=tk.HIDDEN)
            self.canvas.itemconfigure(self.lower_bound_dotid,
                                      state=tk.HIDDEN)

            self.canvas.itemconfigure(self.upper_bound_textid,
                                      state=tk.HIDDEN )

            self.canvas.itemconfigure(self.lower_bound_textid,
                                      state=tk.HIDDEN )


        self.canvas.update()
        self.delay()

    def change_upper_bound(self, value):
        if value == self.upper_bound :
            print('<<與原上限相同，不需改變>>')
            return

        if value <= self.lower_bound :
            print('<<上限需大於下限>>')    

        if not self.puzzle_lower_bound < value < self.puzzle_upper_bound:
            raise 搜尋猜數錯誤("超出題目範圍({}~{})".format(
                                                    self.puzzle_lower_bound,
                                                    self.puzzle_upper_bound))

        ### do  change 
        if self.lower_bound < value < self.upper_bound: 
            # scale shrinks
            for n in range(self.upper_bound, value-1, -1):
                self.draw_ruler(self.lower_bound, n)
            self.upper_bound = value
            # check if bound delta too small
            delta = self.upper_bound - self.lower_bound
            rate = delta /self.ruler_bound_delta
            if rate <= self.ZOOM_IN_RATE:
                for i in range(10):
                    self.delay()
                # # need to do change scale
                # if delta <= self.MIN_SCALE_DELTA:
                #     middle = (self.upper_bound + self.lower_bound)//2
                #     lower_num = middle - self.MIN_SCALE_DELTA//2
                #     upper_num = middle + self.MIN_SCALE_DELTA//2
                #     # border check
                #     if lower_num < self.puzzle_lower_bound:
                #         lower_num = self.puzzle_lower_bound
                #         upper_num = lower_num + self.MIN_SCALE_DELTA
                    
                #     if upper_num > self.puzzle_upper_bound:
                #         upper_num = self.puzzle_upper_bound
                #         lower_num = upper_num - self.MIN_SCALE_DELTA

                #     self.change_scale(lower_num, upper_num)
                self.zoom_in_scale(self.lower_bound, self.upper_bound)


    def change_lower_bound(self, value):
        if value == self.upper_bound or value == self.lower_bound:
            return

        if not self.lower_bound < value < self.upper_bound:
            raise 搜尋猜數錯誤(f"exceed ruler range")

        for n in range(self.lower_bound, value+1):
            self.draw_ruler( n, self.upper_bound)

        self.lower_bound = value

    def zoom_in_scale(self, lower_num ,upper_num):
        if lower_num == self.ruler_lower_bound and upper_num == self.ruler_upper_bound:
            print('<<尺度相同，不需改變>>')
            return

        if self.lower_bound < lower_num or self.upper_bound > upper_num:
            raise 搜尋猜數錯誤("上下限不能在尺度範圍外")

        if lower_num >= upper_num:
            raise 搜尋猜數錯誤("lower_num is bigger")

        # if upper_num - lower_num < self.MIN_SCALE_DELTA:
        #     print('<<尺度差需大於{}>>'.format(self.MIN_SCALE_DELTA))
        #     return

        
        # hide ruler line dot , text .show scale changing text
        self.canvas.itemconfigure(self.ruler_lower_textid,
                                  state=tk.HIDDEN)
        # self.canvas.itemconfigure(self.lower_bound_lineid,
        #                           state=tk.HIDDEN)
        # self.canvas.itemconfigure(self.lower_bound_dotid,
        #                           state=tk.HIDDEN)
        self.canvas.itemconfigure(self.ruler_upper_textid,
                                  state=tk.HIDDEN)
        # self.canvas.itemconfigure(self.upper_bound_lineid,
        #                           state=tk.HIDDEN)
        # self.canvas.itemconfigure(self.upper_bound_dotid,
        #                           state=tk.HIDDEN)
        self.canvas.itemconfigure(self.scale_changing_textid,
                                  state=tk.NORMAL)
        
        
        # temp scale  , for scale change animation
        self.current_color = next(self.COLOR_POOL)
        self.ruler_lower_bound = self.DEFAULT_LOWER_BOUND
        self.ruler_upper_bound = self.DEFAULT_UPPER_BOUND
        self.ruler_bound_delta = self.ruler_upper_bound - self.ruler_lower_bound
        middle = (self.ruler_upper_bound + self.ruler_lower_bound)//2
        for i in range(0,middle, 1):
            self.draw_ruler(middle-i, middle+i, show_gizmo=False)


        # set scale bound and ruler text
        self.canvas.itemconfigure(self.scale_changing_textid,
                                  state=tk.HIDDEN)

        self.ruler_lower_bound = lower_num
        self.ruler_upper_bound = upper_num
        self.ruler_bound_delta = self.ruler_upper_bound - self.ruler_lower_bound
        
        # restore ruler text
        self.canvas.itemconfigure(self.ruler_lower_textid,
                                  state=tk.NORMAL,
                                  text='{}'.format(self.ruler_lower_bound))
        self.canvas.itemconfigure(self.ruler_upper_textid,
                                   state=tk.NORMAL,
                                  text='{}'.format(self.ruler_upper_bound))
        
        #self.draw_ruler(self.lower_bound, self.upper_bound)
        self.draw_ruler(self.ruler_lower_bound, self.ruler_upper_bound)



    def num2y(self, n):
        # number map to coordinate y
        # to do :value check
        tmp =  self.BAR_MAX_Y - (n-self.ruler_lower_bound)* self.BAR_MAX_HEIGHT / self.ruler_bound_delta 
        return int(tmp)

    def gui_init(self):
        self.root = tk.Tk()
        self.small_font = font.Font(size=12, weight=font.NORMAL, family='Consolas')
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
        
        # load arrow 
        path = Path(__file__).parent / 'images' / (self.ARROW_NAME + '.png')     
        _im = Image.open(path)
        self.arrow_img = ImageTk.PhotoImage(_im)
        self.arrow_id = self.canvas.create_image(
                self.ARROW_X,
                self.BAR_MAX_Y,
                image=self.arrow_img,
                anchor=tk.W ,
                state=tk.HIDDEN)

        # test get state (need to be set beforehand)
        # state = self.canvas.itemcget(self.arrow_id, 'state')
        # print('state: ', state)
        

         
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

