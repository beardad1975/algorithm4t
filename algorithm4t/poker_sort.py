import sys
import tkinter as tk
import tkinter.font as font
import random
from PIL import Image, ImageTk
from pathlib import Path
import time

from . import common

class 撲克排序錯誤(Exception):
    pass


class PokerSort:
    ALGORITHM_NAME = "撲克排序"
    DEFAULT_CARD_NUM = 4
    CARD14_NAME_LIST = ['back', 
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
    CARDHOLDER_X = 210
    CARDHOLDER_MIN_Y = 80
    CARDHOLDER_MAX_Y = 700
    CARD_INDEX_X = 320
    INDEX_TITLE_X = 320
    INDEX_TITLE_Y = 70
    INDEX_HIGHTLIGHT = ' <<'
    CARD_WIDTH = 100
    CARD_HEIGHT = 152
    CARD_PREPARE_X = 20
    CARD_PREPARE_Y = 80

    ANIMATE_NUM = 15



    def __init__(self):            
        #self.fold_mode = False
        self.canvas_width = common.poker_canvas_width + 1
        self.canvas_height = common.poker_canvas_height + 1 
        self.card14_img_list = []
        # hand cards related
        
        self.distribute_list = None 
        self.handcards_list = []
        self.index_id_list = []
        #self.cardholders_x_list = []
        self.cardholders_y_list = [] # used by cardholder and index
        self.last_indexes = None
        
    def __getitem__(self, index):
        if not common.current_algorithm ==  self.ALGORITHM_NAME :
            raise 撲克排序錯誤('\n\n要先執行開始發牌後，才能取牌')
            #print("<<取牌無效，請先執行開始發牌>>")
            #return
        
        handcards_num = len(self.distribute_list)

        if type(index) is not int:
            raise 撲克排序錯誤('\n\n索引類型必須是整數')

        if not 0 <= index <= (handcards_num-1):
            raise 撲克排序錯誤('\n\n索引必需為整數0~{}'.format(handcards_num-1))

        self.highlight_indexes([index])
        return self.handcards_list[index]

    def highlight_indexes(self, hi_list):
        if self.last_indexes is not None :
            # remove last hightlight
            for i in self.last_indexes:
                last_id = self.index_id_list[i]
                self.canvas.itemconfigure(last_id, text='['+str(i)+']')
        
        # highlight 
        for i in hi_list:
            index_id = self.index_id_list[i]
            #index_text = self.canvas.itemcget(index_id, 'text')
            self.canvas.itemconfigure(index_id, text='['+str(i)+']' + self.INDEX_HIGHTLIGHT)

        self.last_indexes = hi_list
        self.canvas.update()

    def 開始發牌(self, numOrList = None):
        # algorithm name detect 
        if common.current_algorithm:
            raise 撲克排序錯誤('\n\n'+common.current_algorithm + "演算法已在執行中\n一次只限執行1種演算法")

        common.current_algorithm =  self.ALGORITHM_NAME

        # determine distribute_list( used by handcards later)
        if numOrList is None:
            self.distribute_list = self.random_sample(self.DEFAULT_CARD_NUM)
        elif type(numOrList) is int:
            if numOrList == 0:
                self.distribute_list = self.random_sample(self.DEFAULT_CARD_NUM)
            elif 1 <=  numOrList <= 13:
                self.distribute_list = self.random_sample(numOrList)
            else:
                 raise 撲克排序錯誤("\n\n發牌引數請輸入1~13整數")
        elif type(numOrList) is list :
            if len(numOrList) == 0:
                self.distribute_list = self.random_sample(self.DEFAULT_CARD_NUM)
            elif 1 <= len(numOrList) <= 13:               
                check_point_range = []
                if not all(isinstance(n, int) for n in numOrList):
                    raise 撲克排序錯誤("\n\n發牌引數中，清單內的值都必須是整數") 
                elif not all(1 <= n <= 13 for n in numOrList):
                    raise 撲克排序錯誤("\n\n發牌引數中，清單內的值都必須在1~13內")
                else:
                    # all elements type and value passed
                    self.distribute_list = numOrList[:]

            else:
               raise 撲克排序錯誤("\n\n發牌引數中，清單的數量請在1~13內") 
        else:
            raise 撲克排序錯誤("\n\n發牌引數請輸入1~13整數或清單")
            
        print('發牌: ',self.distribute_list)
        

        # tk and images
        self.gui_init()
        self.calc_cardholder_pos()
        self.prepare_cards()
        #self.show_indexes()
        self.distribute_cards()
        #Card(100,500,6,self)

    def random_sample(self, sample_num):
        one_to_13 = list(range(1,14))
        return random.sample(one_to_13, sample_num)
        
    def calc_cardholder_pos(self):
        handcards_num = len(self.distribute_list)
        assert handcards_num >=0 , 'distribute_list should be positive'
        cardholder_intervals = (self.CARDHOLDER_MAX_Y - self.CARDHOLDER_MIN_Y) // handcards_num
        if cardholder_intervals > self.CARD_HEIGHT :
            cardholder_intervals = self.CARD_HEIGHT + 5

        # TODO : calc index pos

        for i in range(handcards_num):
            self.cardholders_y_list.append(self.CARDHOLDER_MIN_Y + cardholder_intervals * i)

        print('手牌位置: ', self.cardholders_y_list)






    def prepare_cards(self):
        for point in self.distribute_list:
            card = Card(self.CARD_PREPARE_X, self.CARD_PREPARE_Y, point, self)
            card.fold()
            self.handcards_list.append(card)

    def show_indexes(self):
        for i, y in enumerate(self.cardholders_y_list):
            self.canvas.create_text(
                self.CARD_INDEX_X,
                y+10,
                font=self.index_font,
                text='['+str(i)+']',
                anchor=tk.NW,
            )
            self.canvas.update()
            self.delay()
            
    def show_text(self,x, y, text, font):
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
        time.sleep(0.0001)            

    def distribute_cards(self):
        #index title
        self.show_text(self.INDEX_TITLE_X,
                       self.INDEX_TITLE_Y,
                           '索引',
                           self.index_font,
                        )


        handcards_num = len(self.distribute_list)
        for i in range(handcards_num):            
            card = self.handcards_list[i]
            self.move_animate(card, card.x, card.y, self.CARDHOLDER_X, self.cardholders_y_list[i])
            # index
            text_id = self.show_text(self.CARD_INDEX_X,
                           self.cardholders_y_list[i] + 10,
                           '['+str(i)+']',
                           self.index_font,
                        )
            self.index_id_list.append(text_id)


    def move_animate(self, card, x0, y0, x1, y1):
        # move animate card from (x0, y0) to (x1, y1)
        step_x = (x1 - x0) / self.ANIMATE_NUM
        step_y = (y1 - y0) / self.ANIMATE_NUM

        current_x, current_y = x0, y0
        for i in range(self.ANIMATE_NUM-1):
            current_x += step_x
            current_y += step_y
            card.set_position(int(current_x), int(current_y))
            self.delay()
        card.set_position(x1, y1)
        card.show()


    def gui_init(self):
        # tk canvas init
        self.root = tk.Tk()
        self.index_font = font.Font(size=13, weight=font.NORMAL, family='Consolas')
        self.root.geometry("{}x{}+0+0".format(self.canvas_width,self.canvas_height))
        self.canvas = tk.Canvas(self.root, bg = '#c7fcda',
               width=self.canvas_width, height=self.canvas_height,
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

        

        # update at last
        self.canvas.update()

        

    def load_card_images(self):
        for name in self.CARD14_NAME_LIST:
            _im = Image.open(Path(__file__).parent / 'images' / (name + '.png'))       
            self.card14_img_list.append(ImageTk.PhotoImage(_im))

        #print(self.card_img_list)
        
撲克排序 = PokerSort()


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

        self.parent.canvas.update()

    def show(self):        
        self.parent.canvas.itemconfigure(self.cardfront_id, state=tk.NORMAL)
        self.parent.canvas.itemconfigure(self.cardback_id, state=tk.HIDDEN)
        self.folding = False
        self.current_id = self.cardfront_id
                
        self.parent.canvas.coords(self.cardfront_id, self.x, self.y)
        self.parent.canvas.update()

    def 掀牌(self):
        self.show()

    def fold(self):
        self.parent.canvas.itemconfigure(self.cardfront_id, state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(self.cardback_id, state=tk.NORMAL)
        self.folding = True
        self.current_id = self.cardback_id

        self.parent.canvas.coords(self.cardback_id, self.x, self.y)
        self.parent.canvas.update()

    def 蓋牌(self):
        self.fold()

    def set_position(self, x, y):
        width, height = common.poker_canvas_width, common.poker_canvas_height
        if not 0 <= x <= width or not 0 <= y <= height:
            print('<< 座標超過範圍(0~{},0~{})>>'.format(width, height))
            return

        self.x = x 
        self.y = y
        self.parent.canvas.coords(self.current_id, self.x, self.y)
        self.parent.canvas.update()

    def delete(self):
        self.parent.canvas.delete(self.cardfront_id)
        self.parent.canvas.delete(self.cardback_id)
        self.parent.canvas.update()
        del self

    def 交換(self, cardOrIndex):
        pass

    def 插入(self, cardOrIndex):
        pass 

    def 插入在後(self, cardOrIndex):
        pass 

    @property
    def 點數(self):
        return self.point

