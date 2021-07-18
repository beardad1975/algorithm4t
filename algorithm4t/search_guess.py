import sys
import random
import time
import math
from itertools import cycle
from pathlib import Path

import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk

from . import common

class 搜尋猜數錯誤(Exception):
    pass

class BiSearchGuess:
    ALGORITHM_NAME = "搜尋猜數"
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 800

    BACKGROUND_NAME = 'search_guess_bg'
    LOGO_NAME = 'search_guess_logo'
    

    DEFAULT_LOWBOUND = 0
    DEFAULT_UPBOUND = 1000000

    LOGO_X = 50
    LOGO_Y = 0

    PUZZLE_X = 200
    PUZZLE_Y = 80    
    
    def __init__(self):
        self.puzzle_lowbound = None
        self.puzzle_upbound = None
        self.puzzle_answer = None  # bin str
        self.bisearch_ruler = None 
        
    def __repr__(self):
        text = '範圍:{}~{} (次數: , 搜尋:{}, 下限:{}, 上限:{} )'.format(
                                    self.puzzle_lowbound,
                                    self.puzzle_upbound,
                                    self.bisearch_ruler.searcher_num,
                                    self.bisearch_ruler.lowbound,
                                    self.bisearch_ruler.upbound,
                                    )
        return text


    def 產生題目(self, *args, **kwargs):
        if common.current_algorithm is not None and common.current_algorithm != self.ALGORITHM_NAME :
            raise 搜尋猜數錯誤('\n\n'+common.current_algorithm + "演算法已在執行中\n無法同時執行"+self.ALGORITHM_NAME)
        common.current_algorithm =  self.ALGORITHM_NAME

        if len(args) == 0:
            self.puzzle_lowbound = self.DEFAULT_LOWBOUND
            self.puzzle_upbound = self.DEFAULT_UPBOUND

            
                        
            if '隨機種子' in kwargs:
                #print('seed: ', kwargs['隨機種子'])
                random.seed(kwargs['隨機種子'])
            tmp = random.randint(self.puzzle_lowbound,
                            self.puzzle_upbound)
            self.puzzle_answer = bin(tmp)
            #print('answer: ', self.puzzle_answer)

        self.puzzle_text = '範圍{}~{}的整數,請猜答案'.format(
                        self.puzzle_lowbound,self.puzzle_upbound)

        self.puzzle_init()

        #self.canvas.update()

      

    def puzzle_init(self):
        self.gui_init()
        self.set_background()
        self.set_logo()
        self.set_puzzle_note()
        self.bisearch_ruler = BiSearchRuler(self)
        #self.set_assets()
        #self.ruler_init()
        
        #test
        # self.bisearch_ruler.set_lowbound(100)
        # self.bisearch_ruler.set_upbound(109)
        # for i in range(0,3):
        #     r = self.bisearch_ruler.calc_ruler_range(0, 99+i*1)
        #     print(r)
        
        # self.bisearch_ruler.set_upbound(150)
        #self.bisearch_ruler.set_lowbound(196)
        #self.bisearch_ruler.set_searcher(198)
        #self.change_scale(11,80)

    def set_puzzle_note(self):
        
        self.puzzle_id = self.canvas.create_text(
                self.PUZZLE_X,
                self.PUZZLE_Y,
                font=self.normal_font,
                text=self.puzzle_text,
                anchor=tk.CENTER,
                justify=tk.CENTER )

    def gui_init(self):
        self.root = tk.Tk()
        self.scale_font = font.Font(size=10, weight=font.NORMAL, family='Consolas')
        self.small_font = font.Font(size=12, weight=font.NORMAL, family='Consolas')
        self.normal_font = font.Font(size=14, weight=font.NORMAL, family='Consolas')
        self.result_font = font.Font(size=55, weight=font.NORMAL, family='Consolas')
        
        self.root.geometry("{}x{}+0+0".format(self.CANVAS_WIDTH,  self.CANVAS_HEIGHT))
        self.canvas = tk.Canvas(self.root,
                    width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack()

    def set_background(self):
        path = Path(__file__).parent / 'images' / (self.BACKGROUND_NAME + '.png')
                
        _im = Image.open(path)
        self.bg_img = ImageTk.PhotoImage(_im)
        self.bg_id = self.canvas.create_image(
                0,
                0,
                image=self.bg_img,
                anchor=tk.NW)

    def set_logo(self):
        path = Path(__file__).parent / 'images' / (self.LOGO_NAME + '.png')
        
        
        _im = Image.open(path)
        self.logo_img = ImageTk.PhotoImage(_im)
        self.logo_id = self.canvas.create_image(
                self.LOGO_X,
                self.LOGO_Y,
                image=self.logo_img,
                anchor=tk.NW)

    @property
    def 上限(self):
        return self.bisearch_ruler.upbound

    @上限.setter
    def 上限(self, value):
        if type(value) is not int:
            raise 搜尋猜數錯誤('上限值須為整數(錯誤值{})'.format(value))
        
        if not self.puzzle_lowbound<= value <= self.puzzle_upbound:
            raise 搜尋猜數錯誤("超出題目範圍({}~{})".format(
                                                    self.puzzle_lowbound,
                                                    self.puzzle_upbound))

        self.bisearch_ruler.set_upbound(value)

    @property
    def 下限(self):
        return self.bisearch_ruler.lowbound

    @下限.setter
    def 下限(self, value):
        if type(value) is not int:
            raise 搜尋猜數錯誤('下限值須為整數(錯誤值{})'.format(value))
        
        if not self.puzzle_lowbound<= value <= self.puzzle_upbound:
            raise 搜尋猜數錯誤("超出題目範圍({}~{})".format(
                                                    self.puzzle_lowbound,
                                                    self.puzzle_upbound))

        self.bisearch_ruler.set_lowbound(value)

    @property
    def 題目上範圍(self):
        return self.puzzle_upbound

    @property
    def 題目下範圍(self):
        return self.puzzle_lowbound

    @property
    def 答案(self):
        return AnswerCmp(self)


搜尋猜數 = BiSearchGuess()  


class BiSearchRuler:
    RULER_NAME = 'ruler'
    ARROW_NAME = 'search_arrow'
    UP_ROCKET_NAME = 'up_rocket'
    LOW_ROCKET_NAME = 'low_rocket'
    BULB_NAME = 'bulb'

    RULER_X = 150
    RULER_Y = 160

    #COLOR_LIST = ['#349beb','#eb02eb','#11db02','#fc8c03',]
    #COLOR_POOL = cycle(COLOR_LIST)

    BAR_COLOR = '#349beb'
    CHANGE_SCALE_COLOR = '#11db02' 

    SCALE_COLOR = '#969696'

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
    ACTION_X = 183
    ACTION_Y = 730
    BOUND_TEXT_X = 35

    RULER_SCALE_X = 225
    
    ARROW_X = 220
    ARROW_TEXT_X = 300

    COMPARATOR_X = 280
    COMPARATOR_SHIFTY = 65
    BULB_SHIFTY = 50

    LOWBOUND_TEXT_SHIFTY = 8
    UPBOUND_TEXT_SHIFTY = -50

    MIN_SCALE_DELTA = 10
    ZOOM_IN_RATE = 0.05

    ANIMATE_NUM = 80

    def __init__(self, parent):
        self.parent = parent

        low, up = self.calc_ruler_range(self.parent.puzzle_lowbound,
                                        self.parent.puzzle_upbound)
        self.ruler_lowbound = low
        self.ruler_upbound = up
        self.ruler_delta = self.ruler_upbound - self.ruler_lowbound
        

        self.lowbound = self.parent.puzzle_lowbound
        self.upbound = self.parent.puzzle_upbound
       
        self.bar_id = None
        self.thin_bar_id = None
        #self.current_color = next(self.COLOR_POOL)
        self.current_color = self.BAR_COLOR

        self.ruler_scale_id_list = []
        self.searcher_num = None

        
        self.ruler_init()





    def ruler_init(self):

        # put ruler image
        path = Path(__file__).parent / 'images' / (self.RULER_NAME + '.png')     
        _im = Image.open(path)
        self.ruler_img = ImageTk.PhotoImage(_im)
        self.ruler_id = self.parent.canvas.create_image(
                self.RULER_X,
                self.RULER_Y,
                image=self.ruler_img,
                anchor=tk.NW )

        
        self.create_gizmo()

        # create ruler scale text (total 11)
        
        self.create_scale()
        
        # scale changing text
        self.action_textid = self.parent.canvas.create_text(
                self.ACTION_X, 
                self.ACTION_Y,
                anchor=tk.CENTER,
                justify=tk.CENTER,
                state=tk.HIDDEN,
                fill='#d13708',
                font = self.parent.normal_font,
                text='')


        
        # animate draw scale 


        # animate bar from lower bound to upper bound 

        # tmp_step = (self.upbound - self.lowbound)/self.ANIMATE_NUM
        # tmp_upper = self.lowbound
        # for n in range(self.ANIMATE_NUM):
        #     tmp_upper += tmp_step
        #     self.draw_ruler(self.lowbound, round(tmp_upper))
        self.draw_ruler(self.lowbound, self.upbound)
        for i in range(30):
            self.delay()

        self.create_searcher()
        self.create_comparator()

        

    def create_gizmo(self):
        
        # create lower bound line dot and text
        self.lowbound_lineid = self.parent.canvas.create_line(
                self.LINE_X, self.BAR_MAX_Y, 
                self.THIN_BAR_X_RIGHT, self.BAR_MAX_Y,
                fill=self.current_color,
                state=tk.HIDDEN,
                width=2,
                dash=(7,))
        self.lowbound_dotid = self.parent.canvas.create_oval(
                self.LINE_X - 6 , self.BAR_MAX_Y - 6, 
                self.LINE_X + 5, self.BAR_MAX_Y + 5,
                fill=self.current_color,
                state=tk.HIDDEN,
                width=0)
        self.lowbound_textid = self.parent.canvas.create_text(
                self.BOUND_TEXT_X , 
                self.BAR_MAX_Y + self.LOWBOUND_TEXT_SHIFTY,
                anchor=tk.NW,
                justify=tk.CENTER,
                state=tk.HIDDEN,
                font = self.parent.normal_font,
                text='{}\n下限'.format(self.lowbound))
        
        # create upper bound line dot and text
        self.upbound_lineid = self.parent.canvas.create_line(
                self.LINE_X, self.BAR_MAX_Y, 
                self.THIN_BAR_X_RIGHT, self.BAR_MAX_Y,
                fill=self.current_color,
                state=tk.HIDDEN,
                width=2,
                dash=(7,)
                )
        self.upbound_dotid = self.parent.canvas.create_oval(
                self.LINE_X - 6 , self.BAR_MAX_Y - 6, 
                self.LINE_X + 5, self.BAR_MAX_Y + 5,
                fill=self.current_color,
                state=tk.HIDDEN,
                width=0, )
        self.upbound_textid = self.parent.canvas.create_text(
                self.BOUND_TEXT_X , 
                self.BAR_MAX_Y + self.UPBOUND_TEXT_SHIFTY,
                anchor=tk.NW,
                justify=tk.CENTER,
                state=tk.HIDDEN,
                font = self.parent.normal_font,
                text='上限\n{}'.format(self.upbound))


    def set_upbound(self, value):
        if value == self.upbound :
            print('<<與原上限相同，不需改變>>')
            return

        if value <= self.lowbound :
            print('<<上限需大於下限>>') 
            return   

        

        
        if self.ruler_lowbound <= value <= self.ruler_upbound: 
            
            self.change_upbound_in_ruler(value)

            
            

        else:
            # upbound outside ruler
            low, up = self.calc_ruler_range(self.lowbound,
                                            value)
            self.set_ruler_range( low, up)
            self.change_upbound_in_ruler(value)

    def set_lowbound(self, value):
        if value == self.lowbound :
            print('<<與原下限相同，不需改變>>')
            return

        if value >= self.upbound :
            print('<<下限需小於上限>>') 
            return   

        # if not self.puzzle_lower_bound < value < self.puzzle_upper_bound:
        #     raise 搜尋猜數錯誤("超出題目範圍({}~{})".format(
        #                                             self.puzzle_lower_bound,
        #                                             self.puzzle_upper_bound))

        
        if self.ruler_lowbound <= value <= self.ruler_upbound: 
            
            self.change_lowbound_in_ruler(value)

            # if self.check_need_zoomin_scale():
            #     low, up = self.calc_ruler_range(self.lowbound,
            #                                 self.upbound)
            #     self.set_ruler_range( low, up)
            

        else:
            # upbound outside ruler
            low, up = self.calc_ruler_range(value, self.upbound)
            self.set_ruler_range( low, up)
            self.change_lowbound_in_ruler(value)

    def check_need_zoomin_scale(self):
        # check if bound delta too small
        if self.ruler_delta <= 10:
            return False

        delta = self.upbound - self.lowbound
        rate = delta /self.ruler_delta
        if rate < self.ZOOM_IN_RATE:
            return True



    def change_upbound_in_ruler(self, value):
        self.set_action('上限設為{}'.format(value))

        tmp_step = (value - self.upbound ) / self.ANIMATE_NUM
        tmp_upper = self.upbound
        for n in range(self.ANIMATE_NUM):
            tmp_upper += tmp_step
            self.draw_ruler(self.lowbound, round(tmp_upper))
        
        self.upbound = value

    def change_lowbound_in_ruler(self, value):
        self.set_action('下限設為{}'.format(value))

        tmp_step = (value - self.lowbound ) / self.ANIMATE_NUM
        tmp_lower = self.lowbound
        for n in range(self.ANIMATE_NUM):
            tmp_lower += tmp_step
            self.draw_ruler(round(tmp_lower), self.upbound)
        
        self.lowbound = value

    # def set_lowbound(self, value):
    #     if value == self.upbound or value == self.lowbound:
    #         return

    #     if not self.lowbound < value < self.upbound:
    #         raise 搜尋猜數錯誤(f"exceed ruler range")

    #     for n in range(self.lowbound, value+1):
    #         self.draw_ruler( n, self.upbound)

    #     self.lowbound = value

    def set_action(self, text=''):
        self.parent.canvas.itemconfigure(self.action_textid,
                                         text=text,
                                         state=tk.NORMAL)
        self.parent.canvas.update()

    def hide_action(self):
        self.parent.canvas.itemconfigure(self.action_textid,
                                         state=tk.HIDDEN)
        self.parent.canvas.update()

    def set_ruler_range(self, lower_num ,upper_num):
        if lower_num == self.ruler_lowbound and upper_num == self.ruler_upbound:
            #print('<<尺度相同，不需改變>>')
            return

        if self.lowbound < lower_num or self.upbound > upper_num:
            raise 搜尋猜數錯誤("上下限不能在尺度範圍外")

        if lower_num >= upper_num:
            raise 搜尋猜數錯誤("lower_num is bigger")

        # show scale_changing_text

        text = '刻度改為\n{}~{}'.format(lower_num, upper_num)
        self.set_action(text)
        

        self.hide_scale()
        self.hide_searcher()
        self.current_color = self.CHANGE_SCALE_COLOR
        
        #self.current_color = next(self.COLOR_POOL)
        # animate
        old_low_y = self.num2y(self.ruler_lowbound, self.ruler_delta, self.lowbound)
        old_up_y = self.num2y(self.ruler_lowbound, self.ruler_delta, self.upbound)
        new_low_y = self.num2y(lower_num, upper_num-lower_num, self.lowbound)
        new_up_y = self.num2y(lower_num, upper_num-lower_num, self.upbound)
        self.animate_both_bound(old_low_y, old_up_y, new_low_y, new_up_y)   
             

        # set scale bound and ruler text
        self.hide_action()

        self.current_color = self.BAR_COLOR

        # change ruler bounds
        self.ruler_lowbound = lower_num
        self.ruler_upbound = upper_num
        self.ruler_delta = self.ruler_upbound - self.ruler_lowbound
        
        self.draw_scale()
        
        self.draw_ruler(self.lowbound, self.upbound)
        self.set_searcher(self.searcher_num)

        # restore ruler text
        # self.parent.canvas.itemconfigure(self.ruler_lowbound_textid,
        #                           state=tk.NORMAL,
        #                           text='{}'.format(self.ruler_lowbound))
        # self.parent.canvas.itemconfigure(self.ruler_upbound_textid,
        #                            state=tk.NORMAL,
        #                           text='{}'.format(self.ruler_upbound))
        
        #self.draw_ruler(self.lower_bound, self.upper_bound)
        #self.draw_ruler(self.ruler_lowbound, self.ruler_upbound)


    def animate_both_bound(self, old_low_y, old_up_y, new_low_y, new_up_y):
        self.hide_gizmo()

        step_up = (new_up_y - old_up_y)/self.ANIMATE_NUM
        step_low = (new_low_y - old_low_y)/self.ANIMATE_NUM
        big_y, small_y = old_low_y, old_up_y
        for i in range(self.ANIMATE_NUM):
            big_y += step_low
            small_y += step_up
            #print(small_y)
            self.redraw_bar(round(big_y), round(small_y))
            self.parent.canvas.update()
            self.delay()

    def create_scale(self):
        one_10th = self.ruler_delta // 10
        for value in range(self.ruler_lowbound,
                         self.ruler_upbound + one_10th,
                        one_10th):
            y = self.num2y(self.ruler_lowbound, self.ruler_delta, value)
            #print('y: ', y)

            tmp_scale_textid = self.parent.canvas.create_text(
                    self.RULER_SCALE_X  , 
                    y,
                    anchor=tk.W,
                    justify=tk.LEFT,
                    state=tk.NORMAL,
                    font = self.parent.scale_font,
                    fill = self.SCALE_COLOR,
                    text=str(value))
            self.ruler_scale_id_list.append(tmp_scale_textid)
        self.parent.canvas.update()
            
    def hide_scale(self):
        for id in self.ruler_scale_id_list:
            self.parent.canvas.itemconfigure(id, state=tk.HIDDEN)
        self.parent.canvas.update()

    def draw_scale(self):
        one_10th = self.ruler_delta // 10
        for idx, value in enumerate(range(self.ruler_lowbound,
                         self.ruler_upbound + one_10th,
                        one_10th)):
            tmp_scale_textid = self.ruler_scale_id_list[idx]

            self.parent.canvas.itemconfigure(
                    tmp_scale_textid , 
                    state=tk.NORMAL,
                    text=str(value))
        self.parent.canvas.update()

    def create_searcher(self):
        # load arrow
        middle =  self.ruler_lowbound + self.ruler_delta//2
        #self.searcher_num = middle

        y = self.num2y(self.ruler_lowbound, self.ruler_delta, middle)

        path = Path(__file__).parent / 'images' / (self.ARROW_NAME + '.png')     
        _im = Image.open(path)
        self.arrow_img = ImageTk.PhotoImage(_im)
        self.arrow_id = self.parent.canvas.create_image(
                self.ARROW_X,
                y,
                image=self.arrow_img,
                anchor=tk.W ,
                state=tk.NORMAL)

        

        self.arrow_textid = self.parent.canvas.create_text(
                self.ARROW_TEXT_X, 
                y,
                anchor=tk.W,
                justify=tk.LEFT,
                state=tk.NORMAL,
                
                font = self.parent.normal_font,
                text='搜尋')




        self.parent.canvas.update()

    def hide_searcher(self):
        self.parent.canvas.itemconfigure(self.arrow_id, 
                                         state=tk.HIDDEN) 
        self.parent.canvas.itemconfigure(self.arrow_textid, 
                                         state=tk.HIDDEN)
        self.parent.canvas.update()           

    def show_searcher(self):
        self.parent.canvas.itemconfigure(self.arrow_id, 
                                         state=tk.NORMAL)
        self.parent.canvas.itemconfigure(self.arrow_textid, 
                                         state=tk.NORMAL)
        self.parent.canvas.update()

    def set_searcher(self, value):
        if type(value) is not int:
            raise 搜尋猜數錯誤('搜尋數字必需為整數')
        
        #self.set_action('搜尋設為{}'.format(value))
        self.hide_comparator()
        self.searcher_num = value

        if self.ruler_lowbound <= value <= self.ruler_upbound:
            self.draw_searcher(value)

            if self.check_need_zoomin_scale():
                low, up = self.calc_ruler_range(self.lowbound,
                                            self.upbound)
                for i in range(50):
                    self.delay()
                self.set_ruler_range( low, up)

            
        elif value > self.ruler_upbound:
            low, up = self.calc_ruler_range(self.lowbound, value)
            self.set_ruler_range( low, up)
            self.draw_searcher(value)
        elif value < self.ruler_lowbound:
            low, up = self.calc_ruler_range(value, self.upbound)
            self.set_ruler_range( low, up)
            self.draw_searcher(value)


    def draw_searcher(self, value):
        y = self.num2y(self.ruler_lowbound, self.ruler_delta, value)
        self.parent.canvas.coords(self.arrow_id,
                                self.ARROW_X,
                                y)
        self.parent.canvas.itemconfigure(self.arrow_id, 
                                        state=tk.NORMAL)

        self.parent.canvas.coords(self.arrow_textid,
                                self.ARROW_TEXT_X,
                                y)
        self.parent.canvas.itemconfigure(self.arrow_textid,
                                        text='搜尋\n{}'.format(self.searcher_num),
                                        state=tk.NORMAL)
        self.parent.canvas.update()


    def create_comparator(self):
        path = Path(__file__).parent / 'images' / (self.UP_ROCKET_NAME + '.png')     
        _im = Image.open(path)
        self.uprocket_img = ImageTk.PhotoImage(_im)
        self.uprocket_id = self.parent.canvas.create_image(
                0, 0,
                image=self.uprocket_img,
                anchor=tk.CENTER,
                state=tk.HIDDEN)

        path = Path(__file__).parent / 'images' / (self.LOW_ROCKET_NAME + '.png')     
        _im = Image.open(path)
        self.lowrocket_img = ImageTk.PhotoImage(_im)
        self.lowrocket_id = self.parent.canvas.create_image(
                0, 0,
                image=self.lowrocket_img,
                anchor=tk.CENTER,
                state=tk.HIDDEN)

        path = Path(__file__).parent / 'images' / (self.BULB_NAME + '.png')     
        _im = Image.open(path)
        self.bulb_img = ImageTk.PhotoImage(_im)
        self.bulb_id = self.parent.canvas.create_image(
                0, 0,
                image=self.bulb_img,
                anchor=tk.CENTER,
                state=tk.HIDDEN)
        

    def set_comparator(self, op):
        y = self.num2y(self.ruler_lowbound, self.ruler_delta, self.searcher_num)
        
        if op == '>':
            self.parent.canvas.coords(self.uprocket_id,
                                self.COMPARATOR_X ,
                                y - self.COMPARATOR_SHIFTY)
            self.parent.canvas.itemconfigure(self.uprocket_id, 
                                         state=tk.NORMAL)
            
        elif op == '<':
            self.parent.canvas.coords(self.lowrocket_id,
                                self.COMPARATOR_X ,
                                y + self.COMPARATOR_SHIFTY)
            self.parent.canvas.itemconfigure(self.lowrocket_id, 
                                         state=tk.NORMAL)
        elif op == '==':
            self.parent.canvas.coords(self.bulb_id,
                                self.COMPARATOR_X ,
                                y - self.BULB_SHIFTY)
            self.parent.canvas.itemconfigure(self.bulb_id, 
                                         state=tk.NORMAL)       
        self.parent.canvas.update()

    def hide_comparator(self):
        self.parent.canvas.itemconfigure(self.uprocket_id, 
                                         state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(self.lowrocket_id, 
                                         state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(self.bulb_id, 
                                         state=tk.HIDDEN)


    def gt_cmp(self):
        self.set_action('答案大於{}嗎？'.format(self.searcher_num))
        if int(self.parent.puzzle_answer, 2) > self.searcher_num:
            self.set_comparator('>')
            self.delay()
            return True
        else:
            self.delay()
            return False 

    def eq_cmp(self):
        self.set_action('答案等於{}嗎？'.format(self.searcher_num))
        if int(self.parent.puzzle_answer, 2) == self.searcher_num:
            self.set_comparator('==')
            self.delay()
            return True
        else:
            self.delay()
            return False 

    def lt_cmp(self):
        self.set_action('答案小於{}嗎？'.format(self.searcher_num))
        if int(self.parent.puzzle_answer, 2) < self.searcher_num:
            self.set_comparator('<')
            self.delay()
            return True
        else:
            self.delay()
            return False 

    



    def draw_ruler(self, lower_num, upper_num):
        if lower_num > upper_num :
            raise 搜尋猜數錯誤('lowernum > upper_num')

        if type(lower_num) is not int or type(upper_num) is not int:
            raise 搜尋猜數錯誤(' lowernum or upper_num not int')

        big_y = self.num2y(self.ruler_lowbound, self.ruler_delta, lower_num)
        small_y = self.num2y(self.ruler_lowbound, self.ruler_delta, upper_num)

        self.redraw_bar(big_y, small_y)

        # handle both bound text display
            # update upper bound line, dot 
        self.set_gizmo(lower_num ,upper_num, big_y, small_y)

        self.parent.canvas.update()
        self.delay() 





    def redraw_bar(self, big_y, small_y):
        # delete old bar if necessary
        if self.bar_id is not None:
            self.parent.canvas.delete(self.bar_id)
            self.bar_id = None

        if self.thin_bar_id is not None:
            self.parent.canvas.delete(self.thin_bar_id)
            self.thin_bar_id = None

        # redarw bar and thin bar 
        self.bar_id = self.parent.canvas.create_rectangle(
                        self.BAR_X, 
                        small_y,
                        self.BAR_X_RIGHT, 
                        big_y,
                        width=0,    
                        fill=self.current_color,)

        self.thin_bar_id = self.parent.canvas.create_rectangle(
                        self.THIN_BAR_X, 
                        small_y,
                        self.THIN_BAR_X_RIGHT, 
                        big_y,
                        width=0,    
                        fill=self.current_color,)


    def set_gizmo(self, lower_num, upper_num, big_y, small_y):
            self.parent.canvas.coords(self.upbound_lineid, 
                            self.LINE_X, 
                            small_y,
                            self.THIN_BAR_X_RIGHT, 
                            small_y, )
            self.parent.canvas.itemconfigure(self.upbound_lineid,
                            state=tk.NORMAL,
                            fill=self.current_color,)

            self.parent.canvas.coords(self.upbound_dotid,
                    self.LINE_X - 6 , small_y - 6, 
                    self.LINE_X + 5, small_y + 5 )
            self.parent.canvas.itemconfigure(self.upbound_dotid,
                            state=tk.NORMAL,
                            fill=self.current_color,)
            
            # update lower bound line, dot 
            self.parent.canvas.coords(self.lowbound_lineid, 
                            self.LINE_X, 
                            big_y,
                            self.THIN_BAR_X_RIGHT, 
                            big_y, )
            self.parent.canvas.itemconfigure(self.lowbound_lineid,
                            state=tk.NORMAL,
                            fill=self.current_color,)

            self.parent.canvas.coords(self.lowbound_dotid,
                    self.LINE_X - 6 , big_y - 6, 
                    self.LINE_X + 5, big_y + 5 )
            self.parent.canvas.itemconfigure(self.lowbound_dotid,
                            state=tk.NORMAL,
                            fill=self.current_color,)
            

            self.parent.canvas.coords(self.upbound_textid,
                    self.BOUND_TEXT_X , 
                    small_y + self.UPBOUND_TEXT_SHIFTY,)
            self.parent.canvas.itemconfigure(self.upbound_textid,
                    state=tk.NORMAL,
                    text='上限\n{}'.format(upper_num) )

            self.parent.canvas.coords(self.lowbound_textid,
                    self.BOUND_TEXT_X , 
                    big_y + self.LOWBOUND_TEXT_SHIFTY,)
            self.parent.canvas.itemconfigure(self.lowbound_textid,
                    state=tk.NORMAL,
                    text='{}\n下限'.format(lower_num) )



    def hide_gizmo(self):
        # hide line,  dot ,text
        self.parent.canvas.itemconfigure(self.upbound_lineid,
                                    state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(self.upbound_dotid,
                                    state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(self.lowbound_lineid,
                                    state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(self.lowbound_dotid,
                                    state=tk.HIDDEN)

        self.parent.canvas.itemconfigure(self.upbound_textid,
                                    state=tk.HIDDEN )

        self.parent.canvas.itemconfigure(self.lowbound_textid,
                                    state=tk.HIDDEN )






    def num2y(self, lowbound, delta, n):
        # 
        # delta: upbound - lowbound
        # number map to coordinate y
        # to do :value check
        tmp =  self.BAR_MAX_Y - (n - lowbound) * self.BAR_MAX_HEIGHT / delta 
        return int(tmp)      

    def delay(self, sec=0.0001):
        #pass
        time.sleep(sec) 

    def calc_ruler_range(self, lower_num, upper_num):
        # return ruler_low, ruler_up of according to input 
        # base
        # range_exp10:could be 1 2 3 ...

        if upper_num <=  lower_num:
            raise 搜尋猜數錯誤

        #print('--------------')
        #print('low-up: ',lower_num, upper_num)
        delta_exp10 = math.log10(upper_num - lower_num)
        #print('delta: ', upper_num - lower_num)
        #print('delta_exp10: ',delta_exp10)
        
        # calc range_delta
        range_exp10 = math.ceil(delta_exp10)
        if range_exp10 < 1:
            # min exp10 : 1
            range_exp10 = 1

        # calc base
        down_grade = range_exp10 - 1
        if down_grade < 1:
            down_grade = 1
        remainder =  lower_num % (10 ** (down_grade))
        base = int(lower_num - remainder)
        

        # check outside range special case
        if upper_num > base + 10 ** range_exp10 :
            # upgrade exp
            #print('out range : exp10 ++')
            range_exp10 += 1

        #print('base, range_exp10: ', base, range_exp10)
        return base, base + 10 ** range_exp10


class AnswerCmp:
    def __init__(self, parent):
        self.parent = parent

    def __repr__(self):
        return('<<請想一想並動手操作找出答案>>')

    def __gt__(self, other):
        if type(other) is not int:
            raise 搜尋猜數錯誤('比較值須為整數(錯誤值{})'.format(other))       
        
        if not self.parent.puzzle_lowbound<= other <= self.parent.puzzle_upbound:
            raise 搜尋猜數錯誤("超出題目範圍({}~{})，錯誤值{}".format(
                                                    self.parent.puzzle_lowbound,
                                                    self.parent.puzzle_upbound,
                                                    other))

        self.parent.bisearch_ruler.set_searcher(other)
        return self.parent.bisearch_ruler.gt_cmp()

    def __eq__(self, other):
        if type(other) is not int:
            raise 搜尋猜數錯誤('比較值須為整數(錯誤值{})'.format(other))       
        
        if not self.parent.puzzle_lowbound<= other <= self.parent.puzzle_upbound:
            raise 搜尋猜數錯誤("超出題目範圍({}~{})，錯誤值{}".format(
                                                    self.parent.puzzle_lowbound,
                                                    self.parent.puzzle_upbound,
                                                    other))

        self.parent.bisearch_ruler.set_searcher(other)
        return self.parent.bisearch_ruler.eq_cmp()

    def __lt__(self, other):
        if type(other) is not int:
            raise 搜尋猜數錯誤('比較值須為整數(錯誤值{})'.format(other))       
        
        if not self.parent.puzzle_lowbound<= other <= self.parent.puzzle_upbound:
            raise 搜尋猜數錯誤("超出題目範圍({}~{})，錯誤值{}".format(
                                                    self.parent.puzzle_lowbound,
                                                    self.parent.puzzle_upbound,
                                                    other))

        self.parent.bisearch_ruler.set_searcher(other)
        return self.parent.bisearch_ruler.lt_cmp()        