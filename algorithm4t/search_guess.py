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
    DEFAULT_UPBOUND = 100

    LOGO_X = 50
    LOGO_Y = 0

    PUZZLE_X = 200
    PUZZLE_Y = 80    

    ANIMATE_FAST = 25
    ANIMATE_NORMAL = 50
    ANIMATE_SLOW =  100

    RESULT_X = 200
    RESULT_Y = 100
    RESULT_BLINK_TIME = 700
    
    def __init__(self):
        self.puzzle_lowbound = None
        self.puzzle_upbound = None
        self.puzzle_answer = None  # bin str
        self.bisearch_ruler = None
        self.search_guessing = False 
        self.showing_stat = False
        self.animate_num = self.ANIMATE_NORMAL
        
    def __repr__(self):
        text = '範圍:{}~{} (搜尋:{}, 下限:{}, 上限:{})'.format(
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

        if not self.search_guessing:
            self.search_guessing = True
        else:
            print('<<題目已產生>>')
            return

        if len(args) == 0:
            self.puzzle_lowbound = self.DEFAULT_LOWBOUND
            self.puzzle_upbound = self.DEFAULT_UPBOUND
        elif len(args) == 1:
            self.puzzle_lowbound = self.DEFAULT_LOWBOUND

            # check upbound
            upbound = args[0]
            if type(upbound) is not int:
                raise 搜尋猜數錯誤('題目上範圍須為整數(錯誤值{})'.format(upbound))
            
            if upbound <= 0 :
                raise 搜尋猜數錯誤('題目上範圍須為整數(錯誤值{})'.format(upbound))

            self.puzzle_upbound = upbound
        elif len(args) == 2:
            # check 
            lowbound, upbound = args[0], args[1]
            if type(upbound) is not int:
                raise 搜尋猜數錯誤('題目上範圍須為整數(錯誤值{})'.format(upbound))

            if type(lowbound) is not int:
                raise 搜尋猜數錯誤('題目下範圍須為整數(錯誤值{})'.format(lowbound))

            if upbound <= lowbound :
                raise 搜尋猜數錯誤('題目上範圍須大於下範圍)')

            self.puzzle_upbound = upbound
            self.puzzle_lowbound = lowbound

        else:
            raise 搜尋猜數錯誤('引數太多')

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


    def 提交搜尋(self):
        if not self.search_guessing:
            print('<<請先執行 產生題目>>')
            return 

        if not self.bisearch_ruler.searcher_num:
            print('<<請至少搜尋1次(與答案比較)>>')
            return 

        'here'
        if self.bisearch_ruler.searcher_num == int(self.puzzle_answer, 2):
            tmp_text = "搜尋成功"
        else:
            tmp_text = '搜尋失敗\n答案是\n{}'.format(int(self.puzzle_answer, 2))

        self.result_id = self.canvas.create_text(
                self.RESULT_X,
                self.RESULT_Y,
                font=self.result_font,
                text=tmp_text,
                fill='#ff0000',
                anchor=tk.N,
                justify=tk.CENTER, 
        )

        self.result_showing = True
        self.canvas.after(self.RESULT_BLINK_TIME, 
                            self.blink_result)

        self.root.mainloop()

    def blink_result(self):
        
        if self.result_showing:
            self.canvas.itemconfigure(
                            self.result_id,
                            state = tk.HIDDEN
                            ) 
            #print('hidden')        
        else:
            self.canvas.itemconfigure(
                            self.result_id,
                            state = tk.NORMAL
                            )
            #print('normal')
        self.canvas.update()
        self.result_showing = not self.result_showing
        self.canvas.after(self.RESULT_BLINK_TIME,
                            self.blink_result)

    def 設定速度(self, speed):
        if speed == 'normal':
            self.animate_num = self.ANIMATE_NORMAL
            
        elif speed == 'fast':
            self.animate_num = self.ANIMATE_FAST
            
        elif speed == 'slow':
            self.animate_num = self.ANIMATE_SLOW
            
        else:
            raise 排序撲克錯誤("\n\n速度引數應為fast, normal或slow. (錯誤值:{})".format(speed))


    def 顯示統計(self):
        if self.search_guessing:
            self.statistic.show()
        
        self.showing_stat = True


    def 隱藏統計(self):
        if self.search_guessing:
            self.statistic.hide()

        self.showing_stat = True   

      

    def puzzle_init(self):
        self.gui_init()
        self.set_background()
        self.set_logo()
        self.set_puzzle_note()
        self.bisearch_ruler = BiSearchRuler(self)
        self.set_statisic()
        

    def set_puzzle_note(self):
        
        self.puzzle_id = self.canvas.create_text(
                self.PUZZLE_X,
                self.PUZZLE_Y,
                font=self.normal_font,
                text=self.puzzle_text,
                anchor=tk.CENTER,
                justify=tk.CENTER )

    def set_statisic(self):
        self.statistic = Statistic(self)

        if self.showing_stat:
            self.statistic.show()
        else:
            self.statistic.hide()


    def gui_init(self):
        self.root = tk.Tk()
        self.scale_font = font.Font(size=10, weight=font.NORMAL, family='Consolas')
        self.small_font = font.Font(size=12, weight=font.NORMAL, family='Consolas')
        self.normal_font = font.Font(size=14, weight=font.NORMAL, family='Consolas')
        self.result_font = font.Font(size=40, weight=font.NORMAL, family='Consolas')
        
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
        if not self.search_guessing:
            print('<<請先執行 產生題目>>')
            return 
            
        return self.bisearch_ruler.upbound
            

    @上限.setter
    def 上限(self, value):
        if not self.search_guessing:
            print('<<請先執行 產生題目>>')
            return

        # if type(value) is not int:
        #     raise 搜尋猜數錯誤('上限值須為整數(錯誤值{})'.format(value))
        if type(value) is not int:
            print('<<上限值須為整數(錯誤值{})>>'.format(value))
            return
        
        # if not self.puzzle_lowbound<= value <= self.puzzle_upbound:
        #     raise 搜尋猜數錯誤("超出題目範圍({}~{})".format(
        #                                             self.puzzle_lowbound,
        #                                             self.puzzle_upbound))
        if not self.puzzle_lowbound<= value <= self.puzzle_upbound:
            print("<<超出題目範圍({}~{})>>".format(
                                                    self.puzzle_lowbound,
                                                    self.puzzle_upbound))
            return

        # if not self.bisearch_ruler.ruler_lowbound<= value <= self.bisearch_ruler.ruler_upbound:
        #     raise 搜尋猜數錯誤("超出尺刻度範圍({}~{})".format(
        #                                             self.bisearch_ruler.ruler_lowbound,
        #                                             self.bisearch_ruler.ruler_upbound))
        if not self.bisearch_ruler.ruler_lowbound<= value <= self.bisearch_ruler.ruler_upbound:
            print("<<超出尺刻度範圍({}~{})>>".format(
                                                    self.bisearch_ruler.ruler_lowbound,
                                                    self.bisearch_ruler.ruler_upbound))
            return

        self.bisearch_ruler.set_upbound(value)

    @property
    def 下限(self):
        if not self.search_guessing:
            print('<<請先執行 產生題目>>')
            return

        return self.bisearch_ruler.lowbound

    @下限.setter
    def 下限(self, value):
        if not self.search_guessing:
            print('<<請先執行 產生題目>>')
            return

        # if type(value) is not int:
        #     raise 搜尋猜數錯誤('下限值須為整數(錯誤值{})'.format(value))
        if type(value) is not int:
            print('<<下限值須為整數(錯誤值{})>>'.format(value))
            return
        
        # if not self.puzzle_lowbound<= value <= self.puzzle_upbound:
        #     raise 搜尋猜數錯誤("超出題目範圍({}~{})".format(
        #                                             self.puzzle_lowbound,
        #                                             self.puzzle_upbound))
        if not self.puzzle_lowbound<= value <= self.puzzle_upbound:
            print("<<超出題目範圍({}~{})>>".format(
                                                    self.puzzle_lowbound,
                                                    self.puzzle_upbound))
            return

        # if not self.bisearch_ruler.ruler_lowbound<= value <= self.bisearch_ruler.ruler_upbound:
        #     raise 搜尋猜數錯誤("超出尺刻度範圍({}~{})".format(
        #                                             self.bisearch_ruler.ruler_lowbound,
        #                                             self.bisearch_ruler.ruler_upbound))
        if not self.bisearch_ruler.ruler_lowbound<= value <= self.bisearch_ruler.ruler_upbound:
            print("<<超出尺刻度範圍({}~{})>>".format(
                                                    self.bisearch_ruler.ruler_lowbound,
                                                    self.bisearch_ruler.ruler_upbound))
            return

        self.bisearch_ruler.set_lowbound(value)

    @property
    def 題目上範圍(self):
        if not self.search_guessing:
            print('<<請先執行 產生題目>>')
            return

        return self.puzzle_upbound

    @property
    def 題目下範圍(self):
        if not self.search_guessing:
            print('<<請先執行 產生題目>>')
            return

        return self.puzzle_lowbound

    @property
    def 答案(self):
        if not self.search_guessing:
            raise 搜尋猜數錯誤('\n\n答案未產生 請先執行 產生題目')    
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

    #ANIMATE_NUM = 50

    
    

    #CMP_ANIMATE_NUM = 30

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

        # tmp_step = (self.upbound - self.lowbound)/self.parent.animate_num
        # tmp_upper = self.lowbound
        # for n in range(self.parent.animate_num):
        #     tmp_upper += tmp_step
        #     self.draw_ruler(self.lowbound, round(tmp_upper))
        self.draw_ruler(self.lowbound, self.upbound)
        # for i in range(30):
        #     self.delay()

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
        if self.ruler_delta <= self.MIN_SCALE_DELTA:
            return False

        delta = self.upbound - self.lowbound
        rate = delta /self.ruler_delta
        if rate < self.ZOOM_IN_RATE:
            return True



    def change_upbound_in_ruler(self, value):
        self.set_action('上限設為{}'.format(value))

        tmp_step = (value - self.upbound ) / self.parent.animate_num
        tmp_upper = self.upbound
        for n in range(self.parent.animate_num):
            tmp_upper += tmp_step
            self.draw_ruler(self.lowbound, round(tmp_upper))
        
        self.upbound = value

    def change_lowbound_in_ruler(self, value):
        self.set_action('下限設為{}'.format(value))

        tmp_step = (value - self.lowbound ) / self.parent.animate_num
        tmp_lower = self.lowbound
        for n in range(self.parent.animate_num):
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

        step_up = (new_up_y - old_up_y)/self.parent.animate_num
        step_low = (new_low_y - old_low_y)/self.parent.animate_num
        big_y, small_y = old_low_y, old_up_y
        for i in range(self.parent.animate_num):
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
                # for i in range(50):
                #     self.delay()
                
                if low <= value <= up:
                    self.set_ruler_range( low, up)

            
        elif value > self.ruler_upbound:
            assert False, 'should checked'
            # print("<<超出尺刻度範圍({}~{})，錯誤值{}>>".format(
            #                                         self.ruler_lowbound,
            #                                         self.ruler_upbound,
            #                                         other))
            #low, up = self.calc_ruler_range(self.lowbound, value)
            #self.set_ruler_range( low, up)
            #self.draw_searcher(value)
        elif value < self.ruler_lowbound:
            assert False, 'should checked'
            # print("<<超出尺刻度範圍({}~{})，錯誤值{}>>".format(
            #                                         self.ruler_lowbound,
            #                                         self.ruler_upbound,
            #                                         other))
            #low, up = self.calc_ruler_range(value, self.upbound)
            #self.set_ruler_range( low, up)
            #self.draw_searcher(value)


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
        

    def draw_comparator(self, op):

        
        
        y = self.num2y(self.ruler_lowbound, self.ruler_delta, self.searcher_num)
        
        if op == '>':
            self.parent.canvas.itemconfigure(self.uprocket_id, 
                                         state=tk.NORMAL)
            # bigger animate
            new_up_y = y - self.COMPARATOR_SHIFTY
            tmp_step = (y - new_up_y ) / self.parent.animate_num
            tmp_y = y
            for n in range(self.parent.animate_num):
                tmp_y -= tmp_step     

                self.parent.canvas.coords(self.uprocket_id,
                                    self.COMPARATOR_X ,
                                    round(tmp_y))
                self.parent.canvas.update()
                self.delay()
            
            
        elif op == '<':
            self.parent.canvas.itemconfigure(self.lowrocket_id, 
                                         state=tk.NORMAL)

            # smaller animate
            new_low_y = y + self.COMPARATOR_SHIFTY
            tmp_step = (new_low_y - y) / self.parent.animate_num
            tmp_y = y
            for n in range(self.parent.animate_num):
                tmp_y += tmp_step
                self.parent.canvas.coords(self.lowrocket_id,
                                    self.COMPARATOR_X ,
                                    round(tmp_y))
                self.parent.canvas.update()
                self.delay()
            
        elif op == '==':
            self.parent.canvas.itemconfigure(self.bulb_id, 
                                         state=tk.NORMAL)
            # equal animate
            new_up_y = y - self.BULB_SHIFTY
            tmp_step = (y - new_up_y ) / self.parent.animate_num
            tmp_y = y
            for n in range(self.parent.animate_num):
                tmp_y -= tmp_step

                self.parent.canvas.coords(self.bulb_id,
                                    self.COMPARATOR_X ,
                                    round(tmp_y))
                self.parent.canvas.update()
                self.delay()

        else:
            raise 搜尋猜數錯誤('\n\nunknown comparision op')
                   
        self.parent.canvas.update()

    def hide_comparator(self):
        self.parent.canvas.itemconfigure(self.uprocket_id, 
                                         state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(self.lowrocket_id, 
                                         state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(self.bulb_id, 
                                         state=tk.HIDDEN)


    def gt_cmp(self):
        self.parent.statistic.add_search_num(self.searcher_num)
        
        if int(self.parent.puzzle_answer, 2) > self.searcher_num:
            self.set_action('答案大於{}'.format(self.searcher_num))
            self.draw_comparator('>')
            self.delay()
            return True
        else:
            self.set_action('答案不大於{}'.format(self.searcher_num))
            self.delay()
            return False 

    def eq_cmp(self):
        self.parent.statistic.add_search_num(self.searcher_num)
        
        if int(self.parent.puzzle_answer, 2) == self.searcher_num:
            self.set_action('答案等於{}'.format(self.searcher_num))
            self.draw_comparator('==')
            self.delay()
            return True
        else:
            self.set_action('答案不等於{}'.format(self.searcher_num))
            self.delay()
            return False 

    def lt_cmp(self):
        self.parent.statistic.add_search_num(self.searcher_num)
        
        if int(self.parent.puzzle_answer, 2) < self.searcher_num:
            self.set_action('答案小於{}'.format(self.searcher_num))
            self.draw_comparator('<')
            self.delay()
            return True
        else:
            self.set_action('答案不小於{}'.format(self.searcher_num))
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
        if range_exp10 < 2:
            # min exp10 : 1
            range_exp10 = 2

        # calc base
        down_grade = range_exp10 - 1
        if down_grade < 2:
            down_grade = 2
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

        if not self.parent.bisearch_ruler.ruler_lowbound<= other <= self.parent.bisearch_ruler.ruler_upbound:
            raise 搜尋猜數錯誤("超出尺刻度範圍({}~{})，錯誤值{}".format(
                                                    self.parent.bisearch_ruler.ruler_lowbound,
                                                    self.parent.bisearch_ruler.ruler_upbound,
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

        if not self.parent.bisearch_ruler.ruler_lowbound<= other <= self.parent.bisearch_ruler.ruler_upbound:
            raise 搜尋猜數錯誤("超出尺刻度範圍({}~{})，錯誤值{}".format(
                                                    self.parent.bisearch_ruler.ruler_lowbound,
                                                    self.parent.bisearch_ruler.ruler_upbound,
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

        if not self.parent.bisearch_ruler.ruler_lowbound<= other <= self.parent.bisearch_ruler.ruler_upbound:
            raise 搜尋猜數錯誤("超出尺刻度範圍({}~{})，錯誤值{}".format(
                                                    self.parent.bisearch_ruler.ruler_lowbound,
                                                    self.parent.bisearch_ruler.ruler_upbound,
                                                    other))

        self.parent.bisearch_ruler.set_searcher(other)
        return self.parent.bisearch_ruler.lt_cmp()        


class Statistic:
    STAT_X = 390
    STAT_Y = 770

    def __init__(self, parent):
        self.parent = parent
        self.stat_font = font.Font(size=13, weight=font.NORMAL, family='Consolas')
        self.search_list = [] 
        self.last_search = None
        
        tmp_text = '搜尋0個數字'
        

        self.search_id = self.parent.canvas.create_text(
                self.STAT_X,
                self.STAT_Y,
                font=self.stat_font,
                text = tmp_text,
                anchor=tk.NE
        ) 

        self.hide()

    def show(self):
        self.parent.canvas.itemconfigure(
                self.search_id, state=tk.NORMAL)
        self.parent.canvas.update()

    def hide(self):
        self.parent.canvas.itemconfigure(
                self.search_id, state=tk.HIDDEN)
        self.parent.canvas.update()

    def add_search_num(self, value):
        if value in self.search_list:
            #print('<<已搜尋過{}, 不算次數>>'.format(value))
            return
            
        if len(self.search_list) != 0:
            self.last_search = self.search_list[-1]

        self.search_list.append(value)

        if not self.last_search:
            tmp_text = '搜尋{}個數字'.format(
                len(self.search_list)
            )
        else:
            tmp_text = '共搜尋{}個數字(前次搜尋:{})'.format(
                    len(self.search_list),
                    self.last_search,
            )
        


        self.parent.canvas.itemconfigure(self.search_id,
                text = tmp_text
        )
        self.parent.canvas.update()

    