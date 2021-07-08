import sys
import tkinter as tk
import random
from PIL import Image, ImageTk
from pathlib import Path

from . import common

class PokerSort:
    def __init__(self):
        self.card_num = None
        self.default_card_num = 4
        self.distribute_list = None  
        self.fold_mode = False
        self.canvas_width = common.poker_canvas_width + 1
        self.canvas_height = common.poker_canvas_height + 1
        self.card_name_list = ['back',
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

        self.handcards_list = []

        

    def 開始發牌(self, numOrList = None):
        # algorithm detect and register name
        if common.current_algorithm:
            print(common.current_algorithm, " 已在執行中\n一次只限執行1種演算法\n程式中斷")
            sys.exit()
        common.current_algorithm =  "撲克排序"

        # tk and images
        self.gui_init()

        # determine handcards
        if numOrList is None:
            pass
        elif type(numOrList) is int :
            pass
        elif
        self.setup_handcards(numOrList)
        #Card(100,500,6,self)

    def gui_init(self):
        # tk canvas init
        self.root = tk.Tk()
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
        #self.canvas.update()

        

    def load_card_images(self):
        for name in self.card_name_list:
            _im = Image.open(Path(__file__).parent / 'images' / (name + '.png'))       
            self.card_img_list.append(ImageTk.PhotoImage(_im))

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
        img_list = self.parent.card_img_list
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

    def fold(self):
        self.parent.canvas.itemconfigure(self.cardfront_id, state=tk.HIDDEN)
        self.parent.canvas.itemconfigure(self.cardback_id, state=tk.NORMAL)
        self.folding = True
        self.current_id = self.cardback_id

        self.parent.canvas.coords(self.cardback_id, self.x, self.y)
        self.parent.canvas.update()

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