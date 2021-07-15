import sys
import tkinter as tk
import tkinter.font as font
import random
from PIL import Image, ImageTk
from pathlib import Path
import time

from . import common

class 排序撲克錯誤(Exception):
    pass


class PokerSort:
    ALGORITHM_NAME = "排序撲克"
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 800

    BACKGROUND_NAME = 'poker_sort_bg'

    DEFAULT_CARD_NUM = 5
    SPADE14_NAME_LIST = ['back', 
                          'spade1',
                          'spade2',
                          'spade3',
                          'spade4',
                          'spade5',
                          'spade6',
                          'spade7',
                          'spade8',
                          'spade9',
                          'spade10',
                          'spade11',
                          'spade12',
                          'spade13',
                        ]
    HEART14_NAME_LIST = ['back', 
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
    DIAMOND14_NAME_LIST = ['back', 
                          'diamond1',
                          'diamond2',
                          'diamond3',
                          'diamond4',
                          'diamond5',
                          'diamond6',
                          'diamond7',
                          'diamond8',
                          'diamond9',
                          'diamond10',
                          'diamond11',
                          'diamond12',
                          'diamond13',
                        ]
    CLUB14_NAME_LIST = ['back', 
                          'club1',
                          'club2',
                          'club3',
                          'club4',
                          'club5',
                          'club6',
                          'club7',
                          'club8',
                          'club9',
                          'club10',
                          'club11',
                          'club12',
                          'club13',
                        ]
    CARDHOLDER_X = 200
    CARDHOLDER_MIN_Y = 100
    CARDHOLDER_MAX_Y = 680
    CARD_INDEX_X = 310

    PICKOUT_X = 100

    INDEX_TITLE_X = 310
    INDEX_TITLE_Y = 90
    INDEX_HIGHLIGHT = ' <<<'
    COMPARE_HIGHLIGHT = ' 比較'
    SWAP_HIGHLIGHT = ' 交換'
    INSERT_HIGHLIGHT = ' 插入'
    CARD_WIDTH = 100
    CARD_HEIGHT = 152
    CARD_PREPARE_X = 10
    CARD_PREPARE_Y = 640
    CARD_PREPARE_GAP = 5
    LOGO_X = 50
    LOGO_Y = 0
    LOGO_NAME = 'poker_sort_logo'

    CHECK_X = 175
    CHECK_PERIOD_FAST = 0.1 # sec
    CHECK_PERIOD_NORMAL = 0.2
    CHECK_PERIOD_SLOW = 0.4
    RESULT_X = 10
    RESULT_Y = 300
    RESULT_BLINK_TIME = 700 # ms

    ANIMATE_FAST = 10
    ANIMATE_NORMAL = 20
    ANIMATE_SLOW =  40
    MULTI_ANIMATE_FAST = 5
    MULTI_ANIMATE_NORMAL = 10
    MULTI_ANIMATE_SLOW = 20


    #ANIMATE_NUM = 10
    #MULTI_ANIMATE_NUM = 5


    def __init__(self):            
        #self.fold_mode = False
        #self.canvas_width = common.poker_canvas_width + 1
        #self.canvas_height = common.poker_canvas_height + 1
        self.suit_name = 'random'  
        self.card14_name_list = []
        self.card14_img_list = []
        
        self.animate_speed = self.ANIMATE_NORMAL
        self.multi_animate_speed = self.MULTI_ANIMATE_NORMAL
        
        # hand cards related
        
        self.sort_target_list = None 
        self.prepare_cards_list = []
        self.handcards_list = []
        self.handcards_num = 0
        self.index_id_list = []
        #self.cardholders_x_list = []
        self.cardholders_y_list = [] # used by cardholder and index
        self.last_indexes = None
        self.logo_img = None
        self.logo_id = None

        self.poker_sorting = False

        self.showing_stat = False
        self.statistic = None
        self.result_checked_start = None
        self.result_checked_num = 0
        self.result_text_id = None
        self.result_showing = False
        
        self.check_period = self.CHECK_PERIOD_NORMAL

    def __len__(self):
        return self.handcards_num

    def __repr__(self):
        if not self.poker_sorting :
            return "<<請先執行 產生牌組>>"

        card_point_list = [ c.point for c in self.handcards_list]
        return '撲克牌{}張: {} '.format(self.handcards_num, repr(card_point_list))

    def __getitem__(self, idx):
        if not self.poker_sorting :
            raise 排序撲克錯誤('\n\n要先執行 產生牌組')
            #print("<<取牌無效，請先執行開始發牌>>")
            #return

        if self.handcards_num == 0:
            raise 排序撲克錯誤('\n\n要先執行 發牌')
        
        if type(idx) is not int:
            raise 排序撲克錯誤('\n\n索引類型必須是整數. (錯誤值:{})'.format(idx))

        if idx >= 0 and (not 0 <= idx <= (self.handcards_num-1)):
            raise 排序撲克錯誤('\n\n索引值必須為整數0~{}. (錯誤值:{})'.format(
                                                    self.handcards_num-1,
                                                     idx,
                                                    ))
        if idx < 0 and (not -self.handcards_num <= idx <= -1):
            raise 排序撲克錯誤('\n\n索引值必須為整數-{}~-1. (錯誤值:{})'.format(
                                                    self.handcards_num,
                                                     idx,
                                                    ))
        

        if idx < 0 :
            idx = self.handcards_num - ( -idx)

        self.highlight_indexes([idx], self.INDEX_HIGHLIGHT)
        return self.handcards_list[idx]

    def highlight_indexes(self, hi_list, hi_text):
        if self.last_indexes is not None :
            # remove last hightlight
            for i in self.last_indexes:
                last_id = self.index_id_list[i]
                self.canvas.itemconfigure(last_id, text='['+str(i)+']',fill='black')
        
        # highlight 
        for i in hi_list:
            index_id = self.index_id_list[i]
            #index_text = self.canvas.itemcget(index_id, 'text')
            self.canvas.itemconfigure(index_id, text='['+str(i)+']' + hi_text, fill='red')

        self.last_indexes = hi_list
        self.canvas.update()

    def 設定速度(self, speed):
        if speed == 'normal':
            self.animate_speed = self.ANIMATE_NORMAL
            self.multi_animate_speed = self.MULTI_ANIMATE_NORMAL
            self.check_period = self.CHECK_PERIOD_NORMAL
        elif speed == 'fast':
            self.animate_speed = self.ANIMATE_FAST
            self.multi_animate_speed = self.MULTI_ANIMATE_FAST
            self.check_period = self.CHECK_PERIOD_FAST
        elif speed == 'slow':
            self.animate_speed = self.ANIMATE_SLOW
            self.multi_animate_speed = self.MULTI_ANIMATE_SLOW
            self.check_period = self.CHECK_PERIOD_SLOW
        else:
            raise 排序撲克錯誤("\n\n速度引數應為fast, normal或slow. (錯誤值:{})".format(speed))

    def 選擇花色(self, suit_name):
        if self.poker_sorting:
            print('<<選擇花色 需在 開始發牌 之前執行>>')
            return
        else:
            if suit_name in ['spade', 'heart', 'diamond', 'club', 'random']:
                self.suit_name = suit_name
            else:
                raise 排序撲克錯誤('\n\n花色名稱{} 錯誤'.format(suit_name))

    def 產生牌組(self, numOrList=None, 隨機種子=None):
        # algorithm name detect 
        if common.current_algorithm is not None and common.current_algorithm != self.ALGORITHM_NAME :
            raise 排序撲克錯誤('\n\n'+common.current_algorithm + "演算法已在執行中\n無法同時執行"+self.ALGORITHM_NAME)
        common.current_algorithm =  self.ALGORITHM_NAME
        
        if not self.poker_sorting:
            self.poker_sorting = True #  start poker sorting
        else:
            print('<<牌組已產生>>')
            return

        # determine sort_target_list( used by handcards later)
        if numOrList is None:
            self.sort_target_list = self.random_sample(self.DEFAULT_CARD_NUM, 隨機種子)
        elif type(numOrList) is int:
            if 3 <=  numOrList <= 13:
                self.sort_target_list = self.random_sample(numOrList, 隨機種子)
            else:
                 raise 排序撲克錯誤("\n\n發牌引數請輸入3~13的張數範圍內. (錯誤值:{})".format(numOrList))
        elif type(numOrList) is list :
            if 3 <= len(numOrList) <= 13:               
                check_point_range = []
                if not all(isinstance(n, int) for n in numOrList):
                    errmsg = "\n\n發牌引數中，清單的值都必須是整數"
                    errmsg += "\n(錯誤清單:{})".format(repr(numOrList))
                    raise 排序撲克錯誤(errmsg) 
                elif not all(1 <= n <= 13 for n in numOrList):
                    errmsg = "\n\n發牌引數中，清單的值都必須在1~13的點數範圍內"
                    errmsg += "\n(錯誤清單:{})".format(repr(numOrList))
                    raise 排序撲克錯誤(errmsg)
                elif len(set(numOrList)) < 3 :
                    errmsg = "\n\n發牌引數中，清單的值至少要有3個不同"
                    errmsg += "\n(錯誤清單:{})".format(repr(numOrList))
                    raise 排序撲克錯誤(errmsg)
                else:
                    # all elements type and value passed
                    self.sort_target_list = numOrList[:]

            else:
               errmsg = "\n\n發牌引數中，清單內值的個數請在3~13的張數範圍內"
               errmsg += "\n(錯誤清單:{})".format(repr(numOrList)) 
               raise 排序撲克錯誤(errmsg) 
        else:
            raise 排序撲克錯誤("\n\n發牌引數請輸入1~13整數或清單")
            
        #print('發牌: ',self.sort_target_list)
        #self.handcards_num = len(self.sort_target_list)

        self._do_init()

    def _do_init(self):

        # tk and images
        self.gui_init()
        self.set_background()
        self.set_logo()
        self.calc_cardholder_pos()
        self.set_cards()
        self.set_statisic()

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

    def set_statisic(self):
        self.statistic = Statistic(self)

        if self.showing_stat:
            self.statistic.show()
        else:
            self.statistic.hide()
        
        


    def random_sample(self, sample_num, seed=None):
        one_to_13 = list(range(1,14))
        if seed is not None :
            random.seed(seed)
        return random.sample(one_to_13, sample_num)
        
    def calc_cardholder_pos(self):
        sort_target_num = len(self.sort_target_list)
        cardholder_intervals = (self.CARDHOLDER_MAX_Y - self.CARDHOLDER_MIN_Y) // sort_target_num
        if cardholder_intervals > self.CARD_HEIGHT :
            cardholder_intervals = self.CARD_HEIGHT + 5

        for i in range(sort_target_num):
            self.cardholders_y_list.append(self.CARDHOLDER_MIN_Y + cardholder_intervals * i)

    def set_cards(self):
        tmp_list = reversed(self.sort_target_list)
        for idx, point in enumerate(tmp_list):
            card = Card(self.CARD_PREPARE_X, 
                        self.CARD_PREPARE_Y - idx * self.CARD_PREPARE_GAP, 
                        point, 
                        self)
            card.fold()
            self.prepare_cards_list.append(card)
            #self.handcards_list.append(card)

    # def show_indexes(self):
    #     for i, y in enumerate(self.cardholders_y_list):
    #         self.canvas.create_text(
    #             self.CARD_INDEX_X,
    #             y+10,
    #             font=self.index_font,
    #             text='['+str(i)+']',
    #             anchor=tk.NW,
    #         )
    #         self.canvas.update()
    #         self.delay()
            
    def make_text(self,x, y, text, font):
        text_id = self.canvas.create_text(
                x,
                y,
                font=font,
                text=text,
                anchor=tk.NW,
                
            )
        self.canvas.update()
        return text_id   


    def delay(self):
        #pass
        time.sleep(0.0001)            

    def __update(self):
        self.canvas.update()
        print('-- updating --')
        self.root.after(1000, self.__update)

    def 發牌(self, 單張=False):
        # if common.current_algorithm is not None and common.current_algorithm != self.ALGORITHM_NAME:
        #     raise 排序撲克錯誤('\n\n'+common.current_algorithm + "演算法已在執行中\n一次只限執行1種演算法")
        # common.current_algorithm =  self.ALGORITHM_NAME

        if not self.poker_sorting:
            self.產生牌組()


        if len(self.prepare_cards_list) == 0:
            print('<<牌已發完>>')
            return 

        previous_num = self.handcards_num

        if previous_num == 0:
            self.make_text(self.INDEX_TITLE_X,
                            self.INDEX_TITLE_Y,
                            '索引',
                            self.index_font,
                            )

        # determine distribute card num
        if 單張:
            distribute_num = 1
        else:
            distribute_num = len(self.prepare_cards_list)

        for i in range(distribute_num):            
            card = self.prepare_cards_list.pop()
            self.handcards_list.append(card)
            self.handcards_num = len(self.handcards_list)
            self.sort_card_zorder()
            
            self.move_animate(card, card.x, card.y, self.CARDHOLDER_X, self.cardholders_y_list[previous_num + i])
            card.show()
            # index
            text_id = self.make_text(self.CARD_INDEX_X,
                           self.cardholders_y_list[previous_num + i] + 10,
                           '['+str(previous_num + i)+']',
                           self.index_font,
                        )
            self.index_id_list.append(text_id)
        
    def 顯示統計(self):
        if self.poker_sorting:
            self.statistic.show()
        
        self.showing_stat = True


    def 隱藏統計(self):
        if self.poker_sorting:
            self.statistic.hide()

        self.showing_stat = True        

    def 排序結算(self):
        if not self.poker_sorting :
            return "<<請先執行 產生牌組>>"

        if self.prepare_cards_list:
            print('<<結算前，請把牌發完>>')
            return

        self.count_result()  # head/tail order_num
        self.check_animate() # check beside cards
        self.show_result() # blink result and mainloop
        self.root.mainloop()

    def count_result(self):
        num = len(self.sort_target_list)
        forward_sort_list = sorted(self.sort_target_list)
        reversed_sort_list = list(reversed(forward_sort_list))
        card_point_list = [ c.point for c in self.handcards_list]

        # count: head forward
        head_forward_counter = 0
        for i in range(num):
            if forward_sort_list[i] == card_point_list[i]:
                head_forward_counter += 1
            else:
                #print(forward_sort_list)
                #print(card_point_list)
                #print('head forward: ', head_forward_counter)
                break
        #print('head forward: ', head_forward_counter)

        # count: head reverse
        head_reverse_counter = 0
        for i in range(num):
            if reversed_sort_list[i] == card_point_list[i]:
                head_reverse_counter += 1
            else:
                # print(reversed_sort_list)
                # print(card_point_list)
                # print('head reverse: ', head_reverse_counter)
                break
        #print('head reverse: ', head_reverse_counter)

        # count: tail forward
        tail_forward_counter = 0
        for i in reversed(range(num)):
            if forward_sort_list[i] == card_point_list[i]:
                tail_forward_counter += 1
            else:
                # print(forward_sort_list)
                # print(card_point_list)
                # print('tail forward: ', tail_forward_counter)
                break   
        #print('tail forward: ', tail_forward_counter)

        # count: tail reverse
        tail_reverse_counter = 0
        for i in reversed(range(num)):
            if reversed_sort_list[i] == card_point_list[i]:
                tail_reverse_counter += 1
            else:
                # print(reversed_sort_list)
                # print(card_point_list)
                # print('tail reverse: ', tail_reverse_counter)
                break 
        #print('tail reverse: ', tail_reverse_counter)  

        if head_forward_counter > self.result_checked_num:
            self.result_checked_num = head_forward_counter
            self.result_checked_start = "head"

        if head_reverse_counter > self.result_checked_num:
            self.result_checked_num = head_reverse_counter
            self.result_checked_start = "head"

        if tail_forward_counter > self.result_checked_num:
            self.result_checked_num = tail_forward_counter
            self.result_checked_start = "tail"    

        if tail_reverse_counter > self.result_checked_num:
            self.result_checked_num = tail_reverse_counter
            self.result_checked_start = "tail" 

        #print(self.result_checked_start, self.result_checked_num)   

    def check_animate(self):
        if self.result_checked_num <= 0:
            return

        _im = Image.open(Path(__file__).parent / 'images' / 'check.png')
        self.check_img = ImageTk.PhotoImage(_im)

        if self.result_checked_start == 'head':
            for i in range(self.result_checked_num):
                self.canvas.create_image(
                    self.CHECK_X,
                    self.cardholders_y_list[i]+10,
                    image=self.check_img,
                    anchor=tk.NW,
                )
                self.canvas.update()
                time.sleep(self.check_period)
        elif self.result_checked_start == 'tail':
            tail_range = range(self.handcards_num-self.result_checked_num  , self.handcards_num)
            for i in reversed(tail_range):
                self.canvas.create_image(
                    self.CHECK_X,
                    self.cardholders_y_list[i]+10,
                    image=self.check_img,
                    anchor=tk.NW,
                )
                self.canvas.update()
                time.sleep(0.25)
        
    def show_result(self):
        if self.result_checked_num < 0:
            return
        elif 0 <= self.result_checked_num < self.handcards_num:
            result_text = '排序\n{}張'.format(self.result_checked_num)
        elif self.result_checked_num == self.handcards_num :
            result_text = '排序\n完成'

        self.result_id = self.make_text(
                            self.RESULT_X,
                            self.RESULT_Y,
                            result_text,
                            self.result_font,
                            )
        self.canvas.itemconfigure(
                            self.result_id,
                            fill = 'red',
                            justify = tk.CENTER,
                            )
        self.result_showing = True
        self.canvas.after(self.RESULT_BLINK_TIME, 
                            self.blink_result)

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

    def move_animate(self, card, x0, y0, x1, y1):
        # move animate card from (x0, y0) to (x1, y1)
        step_x = (x1 - x0) / self.animate_speed
        step_y = (y1 - y0) / self.animate_speed

        current_x, current_y = x0, y0
        for i in range(self.animate_speed-1):
            current_x += step_x
            current_y += step_y
            card.set_position(int(current_x), int(current_y))
            self.delay()
        card.set_position(x1, y1)
        

    def multimove_animate(self, move_list):
        # move_list  consisted of multi (card, x0, y0, x1, y1)
        
        # make step lsit and current list
        # step_list  consisted of multi (step_x, step_y)
        move_card_num = len(move_list)

        step_x_list = []
        step_y_list = []
        current_x_list = []
        current_y_list = []

        for card, x0, y0, x1, y1 in move_list:
            step_x = (x1 - x0) / self.multi_animate_speed
            step_y = (y1 - y0) / self.multi_animate_speed
            step_x_list.append(step_x)
            step_y_list.append(step_y)

            current_x_list.append(x0)
            current_y_list.append(y0)

        # move multi
        for i in range(self.multi_animate_speed-1):
            for j, (card, x0, y0, x1, y1) in enumerate(move_list):
                current_x_list[j] += step_x_list[j]
                current_y_list[j] += step_y_list[j]
                card.set_position(int(current_x_list[j]) , int(current_y_list[j]) )
            self.delay()

        for card, x0, y0, x1, y1 in move_list:
            card.set_position(x1, y1)    


    def gui_init(self):
        # tk canvas init
        self.root = tk.Tk()
        self.index_font = font.Font(size=13, weight=font.NORMAL, family='Consolas')
        self.result_font = font.Font(size=55, weight=font.NORMAL, family='Consolas')
        
        self.root.geometry("{}x{}+0+0".format(self.CANVAS_WIDTH,self.CANVAS_HEIGHT))
        self.canvas = tk.Canvas(self.root, bg = '#c7fcda',
               width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
               )
        self.canvas.pack()

        #load card images
        self.load_card_images()
        

        #determine cards
        
        ## test image card action
        #for i in range(14):
        #    id = self.canvas.create_image(0,120+ i*40,image=self.card_img_list[i],anchor=tk.NW)
        #elf.canvas.coords(id, 150, 0 )
        #self.canvas.delete(3)
        #self.canvas.itemconfigure(5, state=tk.HIDDEN)

        
        self.canvas.update()
        # update every 1 sec
        #self.root.after(1000, self.__update)


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
        #print('id: ', self.logo_id)

    def load_card_images(self):
        # load according to suit
        if self.suit_name == 'spade':
            self.card14_name_list = self.SPADE14_NAME_LIST
        elif self.suit_name == 'heart':
            self.card14_name_list = self.HEART14_NAME_LIST 
        elif self.suit_name == 'diamond':
            self.card14_name_list = self.DIAMOND14_NAME_LIST
        elif self.suit_name == 'club':
            self.card14_name_list = self.CLUB14_NAME_LIST
        elif self.suit_name == 'random':
            tmp_suit_list = [
                        self.SPADE14_NAME_LIST,
                        self.HEART14_NAME_LIST,
                        self.DIAMOND14_NAME_LIST,
                        self.CLUB14_NAME_LIST,
                    ]
            self.card14_name_list = random.choice(tmp_suit_list)
        else:
            raise 排序撲克錯誤('\n\n花色名稱錯誤. (錯誤值:{})'.format(self.suit_name))

        for name in self.card14_name_list:
            _im = Image.open(Path(__file__).parent / 'images' / (name + '.png'))       
            self.card14_img_list.append(ImageTk.PhotoImage(_im))

        #print(self.card_img_list)

    def swap(self, cardOrIdx1, cardOrIdx2):
        #check argument types
        if isinstance(cardOrIdx1, Card) and isinstance(cardOrIdx2, Card):
            self._do_swap(cardOrIdx1, cardOrIdx2)
        elif isinstance(cardOrIdx1, Card) and isinstance(cardOrIdx2, int):
            if  not 0 <= cardOrIdx2 < self.handcards_num:
                raise 排序撲克錯誤('\n\n交換的索引值範圍要在0~{}. (錯誤值:{})'.format(
                                                    self.handcards_num-1,
                                                    cardOrIdx2,
                                                    ))
            else:
                self._do_swap(cardOrIdx1, self.handcards_list[cardOrIdx2] )
        elif isinstance(cardOrIdx1, int) and isinstance(cardOrIdx2, Card):
            if not 0 <= cardOrIdx1 < self.handcards_num:
                raise 排序撲克錯誤('\n\n交換的索引值範圍要在0~{}. (錯誤值:{})'.format(
                                                    self.handcards_num-1,
                                                    cardOrIdx1,
                                                    ))
            else:
                self._do_swap(self.handcards_list[cardOrIdx1], cardOrIdx2 )
        elif isinstance(cardOrIdx1, int) and isinstance(cardOrIdx2, int):
            if not 0 <= cardOrIdx1 < self.handcards_num or not 0 <= cardOrIdx2 < self.handcards_num:
                raise 排序撲克錯誤('\n\n交換的索引值範圍要在0~{}'.format(self.handcards_num-1))
            else:
                self._do_swap(self.handcards_list[cardOrIdx1], 
                              self.handcards_list[cardOrIdx2] )
        else:
            raise 排序撲克錯誤('\n\n交換的引數必須是牌或索引值')

    def _do_swap(self, card1, card2):
        idx1 = self.handcards_list.index(card1)
        idx2 = self.handcards_list.index(card2)

        if idx1 == idx2 : # same card, no need to swap
            print('<<相同位置不需交換>>')
            return 

        # highlight    
        self.highlight_indexes([idx1, idx2], self.SWAP_HIGHLIGHT)


        # swap in handcards_list
        self.handcards_list[idx1], self.handcards_list[idx2] = \
             self.handcards_list[idx2], self.handcards_list[idx1]


        #print('交換>> ', card1, card2)

        # pick out 2 cards
        move_list = []
        move_list.append(
                    (card1, card1.x, card1.y, self.PICKOUT_X, card1.y))
        move_list.append(
                    (card2, card2.x, card2.y, self.PICKOUT_X, card2.y))
        self.multimove_animate(move_list)
        
        # exchange 2 cards
        move_list = []
        move_list.append(
                    (card1, card1.x, card1.y, card2.x, card2.y))
        move_list.append(
                    (card2, card2.x, card2.y, card1.x, card1.y))
        self.multimove_animate(move_list)

        
        self.sort_card_zorder()

        # back in line
        move_list = []
        move_list.append(
                    (card1, card1.x, card1.y, self.CARDHOLDER_X, card1.y))
        move_list.append(
                    (card2, card2.x, card2.y, self.CARDHOLDER_X, card2.y))
        self.multimove_animate(move_list)       

        # keep record
        self.statistic.swap_add1()

    def insert(self, cardOrIdx1, cardOrIdx2):
        #check argument types
        if isinstance(cardOrIdx1, Card) and isinstance(cardOrIdx2, Card):
            self._do_insert(cardOrIdx1, cardOrIdx2)
        elif isinstance(cardOrIdx1, Card) and isinstance(cardOrIdx2, int):
            if  not 0 <= cardOrIdx2 < self.handcards_num:
                raise 排序撲克錯誤('\n\n插入索引值範圍要在0~{}. (錯誤值:{})'.format(
                                                            self.handcards_num-1,
                                                            cardOrIdx2,
                                                            ))
            else:
                self._do_insert(cardOrIdx1, self.handcards_list[cardOrIdx2] )
        elif isinstance(cardOrIdx1, int) and isinstance(cardOrIdx2, Card):
            if not 0 <= cardOrIdx1 < self.handcards_num:
                raise 排序撲克錯誤('\n\n插入索引值範圍要在0~{}'.format(self.handcards_num-1))
            else:
                self._do_insert(self.handcards_list[cardOrIdx1], cardOrIdx2 )
        elif isinstance(cardOrIdx1, int) and isinstance(cardOrIdx2, int):
            if not 0 <= cardOrIdx1 < self.handcards_num or not 0 <= cardOrIdx2 < self.handcards_num:
                raise 排序撲克錯誤('\n\n插入索引值範圍要在0~{}'.format(self.handcards_num-1))
            else:
                self._do_insert(self.handcards_list[cardOrIdx1], 
                              self.handcards_list[cardOrIdx2] )
        else:
            raise 排序撲克錯誤('\n\n插入的引數必須是牌或索引值')        


    def _do_insert(self, from_card, to_card):
        #  card1 insert to card2
        from_idx = self.handcards_list.index(from_card)
        to_idx = self.handcards_list.index(to_card)

        if from_idx == to_idx : # same card, no need to insert
            print('<<相同位置不需插入>>')
            return

        # highlight    
        self.highlight_indexes([to_idx], self.INSERT_HIGHLIGHT)



        # pick out from card
        move_list = []
        move_list.append(
                    (from_card, from_card.x, from_card.y, self.PICKOUT_X, from_card.y))
        self.multimove_animate(move_list)        

        # move up or down
        move_list = []
        move_list.append(
                    (from_card, from_card.x, from_card.y, self.PICKOUT_X, to_card.y))
        self.multimove_animate(move_list)  

        # insert in handcards_list
        pop_card = self.handcards_list.pop(from_idx)
        new_idx = self.handcards_list.index(to_card)
        if from_idx < to_idx : 
            # all other indexes below from_idx will minus 1 (because pickout from_card)
            self.handcards_list.insert(new_idx + 1, pop_card)
        else:
            self.handcards_list.insert(new_idx, pop_card)

        # move other cards to make a vacancy
        move_list = []
        for idx, card in enumerate(self.handcards_list):
            if card is from_card:
                # from_card need not move here
                continue
            if card.y == self.cardholders_y_list[idx]:
                # remain same pos
                continue           
            move_list.append(
                    (card, card.x, card.y, card.x, self.cardholders_y_list[idx]))
        self.multimove_animate(move_list)

        self.sort_card_zorder()  

        # from_card go_to the vacancy (destination)
        move_list = []
        move_list.append(
                    (from_card, from_card.x, from_card.y, self.CARDHOLDER_X, from_card.y))
        self.multimove_animate(move_list)

        # keep record
        self.statistic.insert_add1()

    def sort_card_zorder(self):
        
        

        if self.handcards_num <= 1:
            #no need for only 1 card
            return

        

        for i in range(self.handcards_num-1):
            
            first_card = self.handcards_list[i]
            second_card = self.handcards_list[i+1]
            #self.canvas.tag_raise(second_card.cardfront_id, first_card.cardfront_id )
            #self.canvas.tag_raise(second_card.cardback_id, first_card.cardback_id )
            self.canvas.tag_raise(second_card.current_id, first_card.current_id )

    @property
    def 未發牌數(self):
        return len(self.prepare_cards_list)


排序撲克 = PokerSort()


class Card:
    def __init__(self, x, y, point, parent):
        self.x = x
        self.y = y
        self.point = point
        self.parent = parent
        self.cardfront_id = None
        self.cardback_id = None
        self.current_id = None
        self.folding = False

        # add card object
        img_list = self.parent.card14_img_list
        self.cardfront_id = self.parent.canvas.create_image(x,y,image=img_list[self.point],anchor=tk.NW)
        self.cardback_id = self.parent.canvas.create_image(x+10,y+10,image=img_list[0],anchor=tk.NW)
        # default 
        self.show()

        self.parent.root.update()

    def __repr__(self):
        idx = self.parent.handcards_list.index(self)
        return '撲克牌(點數:{}, 索引:{}) '.format(self.point, idx)

    def show(self):        
        self.parent.canvas.itemconfigure(self.cardfront_id, state=tk.NORMAL)
        self.parent.canvas.itemconfigure(self.cardback_id, state=tk.HIDDEN)
        self.folding = False
        self.current_id = self.cardfront_id
                
        self.parent.canvas.coords(self.cardfront_id, self.x, self.y)
        self.parent.sort_card_zorder() 
        self.parent.root.update()

    def 掀牌(self):
        self.show()

    def fold(self):
        self.parent.canvas.itemconfigure(self.cardfront_id, state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(self.cardback_id, state=tk.NORMAL)
        self.folding = True
        self.current_id = self.cardback_id

        self.parent.canvas.coords(self.cardback_id, self.x, self.y)
        self.parent.sort_card_zorder() 
        self.parent.root.update()

    def 蓋牌(self):
        self.fold()

    def set_position(self, x, y):
        width, height = self.parent.CANVAS_WIDTH, self.parent.CANVAS_HEIGHT
        if not 0 <= x <= width or not 0 <= y <= height:
            print('<< 座標超過範圍(0~{},0~{})>>'.format(width, height))
            return

        self.x = x 
        self.y = y
        self.parent.canvas.coords(self.current_id, self.x, self.y)
        self.parent.root.update()

    # def delete(self):
    #     self.parent.canvas.delete(self.cardfront_id)
    #     self.parent.canvas.delete(self.cardback_id)
    #     self.parent.root.update()
    #     del self

    def 交換(self, cardOrIndex):
        
        self.parent.swap(self, cardOrIndex)
        

    def 插入到(self, cardOrIndex):
        self.parent.insert(self, cardOrIndex) 

    @property
    def 點數(self):
        return Point(self.point, self, self.parent)

    @property
    def 索引值(self):
        return self.parent.handcards_list.index(self)

class Point(int):
    def __new__(cls, value, card, parent):
        x = int.__new__(cls, value)
        #print('parent: ', parent)
        x.card = card
        x.parent = parent
        return x

    def __eq__(self, other):
        self.parent.statistic.compare_add1()
        #print(self.parent.comparision_num)
        self.highlight_cmp(other)
        return int.__eq__(self, other)

    def __ne__(self, other):
        self.parent.statistic.compare_add1()
        #print(self.parent.comparision_num)
        self.highlight_cmp(other)
        return int.__ne__(self, other)

    def __lt__(self, other):
        self.parent.statistic.compare_add1()
        #print(self.parent.comparision_num)
        self.highlight_cmp(other)
        return int.__lt__(self, other)

    def __gt__(self, other):
        self.parent.statistic.compare_add1()
        #print(self.parent.comparision_num)
        self.highlight_cmp(other)
        return int.__gt__(self, other)

    def __le__(self, other):
        self.parent.statistic.compare_add1()
        #print(self.parent.comparision_num)
        self.highlight_cmp(other)
        return int.__le__(self, other)

    def __ge__(self, other):
        self.parent.statistic.compare_add1()
        #print(self.parent.comparision_num)
        self.highlight_cmp(other)
        return int.__ge__(self, other)

    def highlight_cmp(self, other):
        if isinstance(other, Point):
            idx_list = [self.card.索引值, other.card.索引值]  
        else:
            idx_list = [self.card.索引值]  
        self.parent.highlight_indexes(idx_list, self.parent.COMPARE_HIGHLIGHT)

class Statistic:
    STAT_X = 15
    STAT_Y = 100
    STAT_X_GAP = 30

    def __init__(self, parent):
        self.parent = parent
        self.index_font = font.Font(size=13, weight=font.NORMAL, family='Consolas')

        self.compare_num = 0
        self.compare_name ='比較'
        self.compare_y = self.STAT_Y

        self.swap_num = 0 
        self.swap_name = '交換'
        self.swap_y = self.STAT_Y +self. STAT_X_GAP

        self.insert_num = 0
        self.insert_name = '插入'
        self.insert_y = self.STAT_Y + self.STAT_X_GAP * 2

        self.sep_line_y = self.STAT_Y + self.STAT_X_GAP * 3

        #self.total_num = 0
        self.total_name = '總計'
        self.total_y = self.STAT_Y + int(self.STAT_X_GAP * 3.5)

        self.compare_id = self.parent.canvas.create_text(
                self.STAT_X,
                self.compare_y,
                font=self.index_font,
                text='{:s}: {:d}'.format(self.compare_name,
                                        self.compare_num),
                anchor=tk.NW )

        self.swap_id = self.parent.canvas.create_text(
                self.STAT_X,
                self.swap_y,
                font=self.index_font,
                text='{:s}: {:d}'.format(self.swap_name,
                                        self.swap_num),
                anchor=tk.NW )

        self.insert_id = self.parent.canvas.create_text(
                self.STAT_X,
                self.insert_y,
                font=self.index_font,
                text='{:s}: {:d}'.format(self.insert_name,
                                        self.insert_num),
                anchor=tk.NW )

        self.sep_line_id = self.parent.canvas.create_line(
                 self.STAT_X, self.sep_line_y,
                 self.STAT_X + 70, self.sep_line_y,
                )

        self.total_id = self.parent.canvas.create_text(
                self.STAT_X,
                self.total_y,
                font=self.index_font,
                text='{:s}: {:d}'.format(self.total_name,
                    self.compare_num+self.swap_num+self.insert_num),
                anchor=tk.NW )

        self.hide()

    def show(self):
        # if self.parent.showing_stat:
        #     print('<<統計已顯示>>')
        #     return
        self.parent.canvas.itemconfigure(
                self.compare_id, state=tk.NORMAL)
        self.parent.canvas.itemconfigure(
                self.swap_id, state=tk.NORMAL)
        self.parent.canvas.itemconfigure(
                self.insert_id, state=tk.NORMAL)
        self.parent.canvas.itemconfigure(
                self.sep_line_id, state=tk.NORMAL)
        self.parent.canvas.itemconfigure(
                self.total_id, state=tk.NORMAL)

        self.parent.canvas.update()

    def hide(self):
        # if not self.parent.showing_stat:
        #     print('<<統計已隱藏>>')
        #     return
        self.parent.canvas.itemconfigure(
                self.compare_id, state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(
                self.swap_id, state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(
                self.insert_id, state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(
                self.sep_line_id, state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(
                self.total_id, state=tk.HIDDEN)

        self.parent.canvas.update()

    def compare_add1(self):
        self.compare_num += 1
        self.parent.canvas.itemconfigure(self.compare_id,
                 text='{:s}: {:d}'.format(self.compare_name,
                                        self.compare_num),
                 )

        
        self.parent.canvas.itemconfigure(self.total_id,
                 text='{:s}: {:d}'.format(self.total_name,
                    self.compare_num+self.swap_num+self.insert_num),
                 )
        self.parent.canvas.update()

    def insert_add1(self):
        self.insert_num += 1
        self.parent.canvas.itemconfigure(self.insert_id,
                 text='{:s}: {:d}'.format(self.insert_name,
                                        self.insert_num),
                 )

        
        self.parent.canvas.itemconfigure(self.total_id,
                 text='{:s}: {:d}'.format(self.total_name,
                    self.compare_num+self.swap_num+self.insert_num),
                 )
        self.parent.canvas.update()

    def swap_add1(self):
        self.swap_num += 1
        self.parent.canvas.itemconfigure(self.swap_id,
                 text='{:s}: {:d}'.format(self.swap_name,
                                        self.swap_num),
                 )

        
        self.parent.canvas.itemconfigure(self.total_id,
                 text='{:s}: {:d}'.format(self.total_name,
                    self.compare_num+self.swap_num+self.insert_num),
                 )
        self.parent.canvas.update()
